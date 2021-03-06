from typing import List, Callable
from flask import Blueprint, render_template, request, url_for, abort
from werkzeug.utils import secure_filename
from grc.business_logic.data_store import DataStore
from grc.business_logic.data_structures.uploads_data import UploadsData, EvidenceFile
from grc.upload.forms import UploadForm, DeleteForm
from grc.utils.decorators import LoginRequired
from grc.external_services.aws_s3_client import AwsS3Client
from grc.utils.redirect import local_redirect

upload = Blueprint('upload', __name__)


class UploadSection:
    def __init__(self, url: str, data_section: str, html_file: str, file_list: Callable[[UploadsData], List[EvidenceFile]]):
        self.url = url
        self.data_section = data_section
        self.html_file = html_file
        self.file_list = file_list


sections = [
    UploadSection(url='medical-reports', data_section='medicalReports', html_file='medical-reports.html', file_list=(lambda u: u.medical_reports)),
    UploadSection(url='gender-evidence', data_section='genderEvidence', html_file='evidence.html', file_list=(lambda u: u.evidence_of_living_in_gender)),
    UploadSection(url='name-change', data_section='nameChange', html_file='name-change.html', file_list=(lambda u: u.name_change_documents)),
    UploadSection(url='marriage-documents', data_section='marriageDocuments', html_file='marriage-documents.html', file_list=(lambda u: u.partnership_documents)),
    UploadSection(url='overseas-certificate', data_section='overseasCertificate', html_file='overseas-certificate.html', file_list=(lambda u: u.overseas_documents)),
    UploadSection(url='statutory-declarations', data_section='statutoryDeclarations', html_file='statutory-declarations.html', file_list=(lambda u: u.statutory_declarations))
]


@upload.route('/upload/<section_url>', methods=['GET', 'POST'])
@LoginRequired
def uploadInfoPage(section_url: str):
    section = next(filter(lambda section: section.url == section_url, sections), None)
    if section is None:
        abort(404)

    form = UploadForm()
    deleteform = DeleteForm()
    application_data = DataStore.load_application_by_session_reference_number()
    files = section.file_list(application_data.uploads_data)

    if form.validate_on_submit():
        if form.button_clicked.data == 'Upload file':
            for document in request.files.getlist('documents'):
                filename = secure_filename(document.filename)
                object_name = application_data.reference_number + '__' + section.data_section + '__' + filename
                AwsS3Client().upload_fileobj(document, object_name)

                new_evidence_file = EvidenceFile()
                new_evidence_file.original_file_name = document.filename
                new_evidence_file.aws_file_name = object_name
                files.append(new_evidence_file)

            DataStore.save_application(application_data)

            return local_redirect(url_for('upload.uploadInfoPage', section_url=section.url) + '#file-upload-section')

        elif form.button_clicked.data == 'Save and continue':
            if len(files) > 0:
                return local_redirect(url_for('taskList.index'))
            else:
                form.documents.errors.append('Select a JPG, BMP, PNG, TIF or PDF file smaller than 10MB')

    return render_template(
        f"upload/{section.html_file}",
        form=form,
        deleteform=deleteform,
        section_url=section.url,
        currently_uploaded_files=files
    )


@upload.route('/upload/<section_url>/remove-file', methods=['POST'])
@LoginRequired
def removeFile(section_url: str):
    section = next(filter(lambda section: section.url == section_url, sections), None)
    if section is None:
        abort(404)

    form = DeleteForm()
    application_data = DataStore.load_application_by_session_reference_number()

    if form.validate_on_submit():
        AwsS3Client().delete_object(form.file.data)
        files = section.file_list(application_data.uploads_data)
        file_to_remove = next(filter(lambda file: file.aws_file_name == form.file.data, files), None)
        files.remove(file_to_remove)
        DataStore.save_application(application_data)

    return local_redirect(url_for('upload.uploadInfoPage', section_url=section.url) + '#file-upload-section')
