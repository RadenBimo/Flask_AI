from flask import Blueprint
from controllers.UserController import UserController
from controllers.PdfController import PdfController

api = Blueprint('api', __name__)

# Instantiate controllers
userController = UserController()
pdfController = PdfController()

# User routes
api.route('/register', methods=['POST'])(userController.register)
api.route('/login', methods=['POST'])(userController.login)
api.route('/user/update', methods=['PUT'])(userController.update)
api.route('/user/delete', methods=['DELETE'])(userController.delete)

# PDF routes (CRUD operations)
api.route('/pdfs', methods=['POST'])(pdfController.upload_pdf)
api.route('/pdfs/<int:id_pdf>', methods=['GET'])(pdfController.get_pdf)
api.route('/pdfs/<int:id_pdf>', methods=['PUT'])(pdfController.update_pdf)
api.route('/pdfs/<int:id_pdf>', methods=['DELETE'])(pdfController.delete_pdf)
api.route('/pdfs', methods=['GET'])(pdfController.list_pdfs)
