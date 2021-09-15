from flask import Flask
from flask_restful import Api
from flask_cors import CORS
from flask_lambda import FlaskLambda

from controllers.masterData import (
    HealthCheck,
    MainInfo,
    InsertJobinterest,
    InsertSchooldata,
    InsertBlocks,
    InsertInterests,
)
from controllers.demographicData import (
    StateSearch,
    DistrictSearch,
    SchoolSearch,
    JobLevellist,
    JobRolelist,
)
from controllers.blockData import (
    ListBlocks,
    ListBuckets,
    GetResourceDescription,
    GetResources,
)
from controllers.users import UserCreate, UserUpdate, GetUser, GetUserInterests
from datamodels.models import CreateTables
from controllers.notes import (
    ListNotes,
    DeleteNote,
    CreateNote,
    SavedNotes,
    LastNotesSaved,
    GenerateNotesPdf,
    NoteTimestamp,
)
from decorators.validation import ValidationError, API_ERROR


app = FlaskLambda(__name__)

app.register_error_handler(
    ValidationError,
    lambda e: API_ERROR(
        e.message,
        e.error,
    ),
)

CORS(app, send_wildcard=True)
api = Api(app)

##MASTER DATA APIs
api.add_resource(HealthCheck, "/api/health-check")
api.add_resource(MainInfo, "/api/main-info")
api.add_resource(CreateTables, "/api/create-tables")
api.add_resource(InsertJobinterest, "/api/insert-job-interest")
api.add_resource(InsertSchooldata, "/api/insert-schools")
api.add_resource(InsertBlocks, "/api/insert-blocks")
api.add_resource(InsertInterests, "/api/insert-interests")

##DEMOGRAPHIC DATA APIs
api.add_resource(ListBlocks, "/api/list-blocks")
api.add_resource(ListBuckets, "/api/list-buckets")
api.add_resource(
    GetResourceDescription,
    "/api/get-resource-description/<string:block_slug>/<string:bucket_slug>/<string:element_slug>",
)
api.add_resource(GetResources, "/api/get-resources")
api.add_resource(StateSearch, "/api/state-search")
api.add_resource(DistrictSearch, "/api/district-search/<string:state_id>")
api.add_resource(SchoolSearch, "/api/school-search/<string:district_id>")
api.add_resource(JobLevellist, "/api/job-level")
api.add_resource(JobRolelist, "/api/job-role/<string:job_id>")

##USER APIs
api.add_resource(UserCreate, "/api/user-create")
api.add_resource(UserUpdate, "/api/user-update")
api.add_resource(GetUser, "/api/get-user/<string:user_id>")
api.add_resource(GetUserInterests, "/api/get-user-interests/<string:user_id>")

##NOTE APIs
api.add_resource(CreateNote, "/api/create-notes")
api.add_resource(ListNotes, "/api/list-notes")
api.add_resource(
    SavedNotes,
    "/api/saved-notes/<string:user_id>/<string:bucket_slug>/<string:element_slug>",
)
api.add_resource(LastNotesSaved, "/api/last-saved-notes/<string:user_id>")
api.add_resource(GenerateNotesPdf, "/api/generate-notes-pdf")
api.add_resource(DeleteNote, "/api/del-note/<string:note_id>")
api.add_resource(NoteTimestamp, "/api/note-time-stamp/<string:user_id>/<string:block_slug>")


if __name__ == "__main__":
    app.run(debug=True)
