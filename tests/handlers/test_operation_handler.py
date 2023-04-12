import json
import pytest
from src.handlers import operation_handler
from src.controller.operation_controller import OperationController


class TestOperationHandler:
    def test_create_operation_handler(self, mocker):
        expected = {
            "message": "OK"
        }

        mocker.patch.object(OperationController, 'create_operation')
        OperationController.create_operation.return_value = {
            "message": "OK"
        }

        response = operation_handler.create_operation_handler({}, None)

        assert json.loads(response["body"]) == expected
        assert response["statusCode"] == 201

    def test_update_operation_handler(self, mocker):
        expected = {
            "message": "OK"
        }

        mocker.patch.object(OperationController, 'update_operation')
        OperationController.update_operation.return_value = {
            "message": "OK"
        }

        response = operation_handler.update_operation_handler({}, None)

        assert json.loads(response["body"]) == expected
        assert response["statusCode"] == 200

    def test_operation_list_handler(self, mocker):
        expected = {
            "message": "OK"
        }

        mocker.patch.object(OperationController, 'get_operation_list')
        OperationController.get_operation_list.return_value = {
            "message": "OK"
        }

        response = operation_handler.get_operation_list_handler({}, None)

        assert json.loads(response["body"]) == expected
        assert response["statusCode"] == 200
