import re
import pdfkit
import base64
from datetime import datetime
from flask import Flask, render_template
from flask import request
from flask_restful import Resource
from datamodels.notesFactory import Notes
from datamodels.userFactory import User
from decorators.auth import authorize
from xhtml2pdf import pisa
from io import BytesIO
from decorators.validation import ValidateRequest
from kanpai import Kanpai

app = Flask(__name__)

# api for creating, updating of notes
class CreateNote(Resource):

    REQUEST_SCHEMA = Kanpai.Object(
        {
            "user_id": Kanpai.String().trim().required("User Id is required"),
            "block_slug": Kanpai.String().required().required("block_slug is required"),
            "bucket_slug": Kanpai.String()
            .required()
            .required("bucket_slug is required"),
            "element_slug": Kanpai.String().required("element_slug is required"),
            "note_type": Kanpai.String().required("note_type is required"),
            "note": Kanpai.String().required("note is required"),
            "note_id": Kanpai.String(),
        }
    )

    @authorize
    @ValidateRequest(schema=REQUEST_SCHEMA)
    def post(self, dynamodb=None):
        try:
            args = request.validated_json
            response = Notes.add_note(args)
            return {
                "status_text": "success",
                "data": "Note Has been created successfully",
            }, 201
        except Exception as err:
            return {
                "status_text": "error",
                "data": "HTTPStatusCode:{}, {}".format(
                    err.response["ResponseMetadata"]["HTTPStatusCode"], err
                ),
            }, 500

    @authorize
    @ValidateRequest(schema=REQUEST_SCHEMA)
    def put(self, dynamodb=None):
        args = request.validated_json
        try:
            response = Notes.edit_note(args)
            return {
                "status_text": "success",
                "data": "Note has been updated successfully",
            }, 201
        except Exception as err:
            return {
                "status_text": "error",
                "data": "HTTPStatusCode:{}, {}".format(
                    err.response["ResponseMetadata"]["HTTPStatusCode"], err
                ),
            }, 500


# api for deleying the note created by user
class DeleteNote(Resource):
    def delete(self, note_id, dynamodb=None):
        try:
            response = Notes.del_note(note_id)
            return {
                "status_text": "success",
                "data": "Note has been deleted successfully",
            }, 201
        except Exception as err:
            return {
                "status_text": "error",
                "data": "HTTPStatusCode:{}, {}".format(
                    err.response["ResponseMetadata"]["HTTPStatusCode"], err
                ),
            }, 500


# api for displaying the saved notes in element page
class SavedNotes(Resource):
    @authorize
    def get(self, user_id, bucket_slug, element_slug):
        try:
            note_list = Notes.list_notes(user_id)
            matched_note_list = list(
                filter(
                    lambda item: item["bucket_slug"] == bucket_slug
                    and item["element_slug"] == element_slug,
                    note_list,
                )
            )

            matched_note_list.sort(
                key=lambda item: datetime.strptime(
                    item["created_date"], "%d %B %Y %I:%M %p"
                ),
                reverse=True,
            )

            return {"status_text": "success", "data": matched_note_list}, 200
        except Exception as err:
            return {
                "status_text": "error",
                "data": "HTTPStatusCode:{}, {}".format(
                    err.response["ResponseMetadata"]["HTTPStatusCode"], err
                ),
            }, 500


# api for listing already created notes by user, sorting the notes, and filtering the notes
class ListNotes(Resource):
    @authorize
    def get(self):
        try:
            filtersort_args = request.args
            sorted_note = self.sort_notes(filtersort_args)
            filter_note = self.filter_notes(filtersort_args, sorted_note)
            return {"status_text": "success", "data": filter_note}, 201
        except Exception as err:
            return {
                "status_text": "error",
                "data": "HTTPStatusCode:{}, {}".format(
                    err.response["ResponseMetadata"]["HTTPStatusCode"], err
                ),
            }, 500

    def filter_notes(self,args, sorted_note):
        filtered_note = sorted_note
        block_slug = args.get("block_slug")
        if block_slug:
            filtered_note = list(
                filter(lambda item: item["block_slug"] == block_slug, filtered_note)
            )

        note_type = args.get("note_type")
        if note_type:
            filtered_note = list(
                filter(lambda item: item["note_type"] == note_type, filtered_note)
            )

        start_date = args.get("start_date")
        end_date = args.get("end_date")
        if start_date and end_date:
            dt_from_str = lambda dt: datetime.strptime(dt, "%d %B %Y")
            first_date = dt_from_str(start_date)
            second_date = dt_from_str(end_date)
            for notes in filtered_note:
                notes["time"] = notes["created_date"]
                notes["created_date"] = re.sub(
                    "\s\s\d{2}:\d{2}\s\D{2}", "", notes["created_date"]
                )

            filter_note = list(
                filter(
                    lambda item: first_date
                    <= datetime.strptime(item["created_date"], "%d %B %Y")
                    <= second_date,
                    filtered_note,
                )
            )
            filtered_note = list(
                map(
                    lambda item: {
                        "user_id": item["user_id"],
                        "block_slug": item["block_slug"],
                        "element_slug": item["element_slug"],
                        "note_type": item["note_type"],
                        "note_id": item["note_id"],
                        "note": item["note"],
                        "created_date": item["time"],
                    },
                    filter_note,
                )
            )
        return filtered_note

    def sort_notes(self,args):
        user_id = args.get("user_id")
        sort_order = args.get("sort_order")
        note_list = Notes.list_notes(user_id)
        if sort_order == "newest":
            note_list.sort(
                key=lambda item: datetime.strptime(
                    item["created_date"], "%d %B %Y %I:%M %p"
                ),
                reverse=True,
            )
        elif sort_order == "oldest":
            note_list.sort(
                key=lambda item: datetime.strptime(
                    item["created_date"], "%d %B %Y %I:%M %p"
                )
            )
        return note_list


class GenerateNotesPdf(Resource):
    
    WKHTMLTOPDF_PATH = (
        app.root_path + "/wkhtmltox-0.12.6-4.amazonlinux2_lambda/bin/wkhtmltopdf"
    )
    @authorize
    def get(self):
        try:
            user = User.user_get(request.args.get("user_id"))
        except:
            return {
                "status_text": "error",
                "error_text": "Invalid user id",
            }, 500
        filtersort_args = request.args
        sorted_note = ListNotes.sort_notes(filtersort_args)
        filter_note = ListNotes.filter_notes(filtersort_args, sorted_note)
        pdf = self.render_pdf_xhtml2pdf(filter_note, user)
        print(type(pdf))
        return {
            "statusCode": 200,
            "headers": {
                "Content-Type": "application/pdf",
                "Content-Disposition": "inline; filename=output.pdf"
            },
            "body": base64.b64encode(pdf).decode('utf-8'),
            "isBase64Encoded": True

        }

    def generate_pdf(self, notes, user):

        pdf_data = {"user": user["Item"], "notes": notes, "date" :datetime.now()}
        html = render_template('export-notes.html', data=pdf_data)
        config = pdfkit.configuration()
        pdf = pdfkit.from_string(html, False)
        return pdf
    
    def render_pdf_xhtml2pdf(self, notes, user):
        """mimerender helper to render a PDF from HTML using xhtml2pdf.
        Usage: http://philfreo.com/blog/render-a-pdf-from-html-using-xhtml2pdf-and-mimerender-in-flask/
        """
        
        pdf_data = {"user": user["Item"], "notes": notes, "date" :datetime.now()}
        html = render_template('export-notes.html', data=pdf_data)
        pdf = BytesIO()
        pisa.CreatePDF(BytesIO(html.encode("utf-8")), pdf)
        resp = pdf.getvalue()

        pdf.close()
        return resp


# displaying the elements with latest saved notes
class LastNotesSaved(Resource):
    @authorize
    def get(self, user_id):
        try:
            saved_list = Notes.list_notes(user_id)
            last_saved_notes = list(
                map(
                    lambda item: {
                        "block_slug": item["block_slug"],
                        "bucket_slug": item["bucket_slug"],
                        "element_slug": item["element_slug"],
                        "created_date": item["created_date"],
                    },
                    saved_list,
                )
            )
            last_saved_notes.sort(
                key=lambda item: datetime.strptime(
                    item["created_date"], "%d %B %Y %I:%M %p"
                ),
                reverse=True,
            )
            if len(last_saved_notes) > 6:
                last_savedlist = last_saved_notes[0:7]
            else:
                last_savedlist = last_saved_notes

            return {
                "status_text": "success",
                "error_text": {},
                "data": last_savedlist,
            }, 200

        except Exception as err:
            return {
                "status_text": "error",
                "data": "HTTPStatusCode:{}, {}".format(
                    err.response["ResponseMetadata"]["HTTPStatusCode"], err
                ),
            }, 500


#API for displaying timestamp of notes with the element name
class NoteTimestamp(Resource):
    # @authorize
    def get(self, user_id, block_slug):
        try:
            saved_list = Notes.list_notes(user_id)
            matched_notes = list(
                filter(lambda item: item["block_slug"] == block_slug, saved_list)
            )
            last_saved_notes = list(
                map(
                    lambda item: {
                        "bucket_slug": item["bucket_slug"],
                        "element_slug": item["element_slug"],
                        "created_date": item["created_date"],
                    },
                    matched_notes,
                )
            )
            last_saved_notes.sort(
                key=lambda item: datetime.strptime(
                    item["created_date"], "%d %B %Y %I:%M %p"
                ),
                reverse=True,
            )
            return {
                "status_text": "success",
                "error_text": {},
                "data": last_saved_notes,
            }, 200

        except Exception as err:
            return {
                "status_text": "error",
                "data": "HTTPStatusCode:{}, {}".format(
                    err.response["ResponseMetadata"]["HTTPStatusCode"], err
                ),
            }, 500
