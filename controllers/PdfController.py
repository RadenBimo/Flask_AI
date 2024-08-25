import os
from flask import request, jsonify, current_app
from flask_jwt_extended import jwt_required, get_jwt_identity
from werkzeug.utils import secure_filename
from app import db
from models.Pdf import Pdf

class PdfController:

    @jwt_required()
    def upload_pdf(self):
        current_user_id = get_jwt_identity()

        if 'file' not in request.files:
            return jsonify({"message": "No file part in the request"}), 400

        file = request.files['file']

        if file.filename == '':
            return jsonify({"message": "No selected file"}), 400

        if file:
            filename = secure_filename(file.filename)
            file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)

            new_pdf = Pdf(
                id_user=current_user_id,
                file_name=filename,
                file_path=file_path,
                description=request.form.get('description', ''),
                tag=request.form.get('tag', '')
            )
            db.session.add(new_pdf)
            db.session.commit()

            return jsonify({"message": "PDF uploaded successfully", "pdf_id": new_pdf.id_pdf}), 201

    @jwt_required()
    def get_pdf(self, id_pdf):
        current_user_id = get_jwt_identity()
        pdf = Pdf.query.filter_by(id_pdf=id_pdf, id_user=current_user_id).first()

        if not pdf:
            return jsonify({"message": "PDF not found"}), 404

        return jsonify({
            "id_pdf": pdf.id_pdf,
            "file_name": pdf.file_name,
            "file_path": pdf.file_path,
            "description": pdf.description,
            "tag": pdf.tag
        }), 200

    @jwt_required()
    def update_pdf(self, id_pdf):
        current_user_id = get_jwt_identity()
        pdf = Pdf.query.filter_by(id_pdf=id_pdf, id_user=current_user_id).first()

        if not pdf:
            return jsonify({"message": "PDF not found"}), 404

        data = request.form
        pdf.description = data.get('description', pdf.description)
        pdf.tag = data.get('tag', pdf.tag)

        if 'file' in request.files:
            file = request.files['file']
            filename = secure_filename(file.filename)
            file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)
            pdf.file_name = filename
            pdf.file_path = file_path

        db.session.commit()

        return jsonify({"message": "PDF updated successfully"}), 200

    @jwt_required()
    def delete_pdf(self, id_pdf):
        current_user_id = get_jwt_identity()
        pdf = Pdf.query.filter_by(id_pdf=id_pdf, id_user=current_user_id).first()

        if not pdf:
            return jsonify({"message": "PDF not found"}), 404

        db.session.delete(pdf)
        db.session.commit()

        # Optionally delete the file from the filesystem
        if os.path.exists(pdf.file_path):
            os.remove(pdf.file_path)

        return jsonify({"message": "PDF deleted successfully"}), 200

    @jwt_required()
    def list_pdfs(self):
        current_user_id = get_jwt_identity()
        pdfs = Pdf.query.filter_by(id_user=current_user_id).all()

        return jsonify([{
            "id_pdf": pdf.id_pdf,
            "file_name": pdf.file_name,
            "file_path": pdf.file_path,
            "description": pdf.description,
            "tag": pdf.tag
        } for pdf in pdfs]), 200
