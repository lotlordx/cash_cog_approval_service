import datetime
from typing import List
from flask import jsonify
from sqlalchemy import or_, and_
from app.currency_app.models import CurrencyModel
from app.employee_app.models import EmployeeModel
from .schema import TransactionSchema
from .models import TransactionModel


class TransactionServices:

    def __init__(self):
        self.schema = TransactionSchema()
        self.service_model = TransactionModel
        self.currency_model = CurrencyModel
        self.employee_model = EmployeeModel
        self.page_no = 1
        self.page_size = 100

    def get_all_records(self, request) -> List[TransactionModel]:
        search_conditions = []
        page_no = request.args.get('page_no', self.page_no)
        page_size = request.args.get('page_size', self.page_size)
        search_by_approval_status = request.args.get('approval_status', None)
        search_by_currency = request.args.get('currency', None)
        search_by_description = request.args.get('description', None)
        search_by_employee_first_name = request.args.get('employee_first_name', None)
        search_by_employee_last_name = request.args.get('employee_last_name', None)
        search_by_employee_uuid = request.args.get('employee_uuid', None)
        offset = (int(page_no) - 1) * int(page_size)

        if search_by_approval_status is not None and search_by_approval_status:
            search_conditions.append(self.service_model.approval_status == search_by_approval_status)
        if search_by_currency is not None and search_by_currency:
            search_conditions.append(self.currency_model.currency_code == search_by_currency)
        if search_by_description is not None and search_by_description:
            search_conditions.append(self.service_model.description.contains(search_by_description))
        if search_by_employee_first_name is not None and search_by_employee_first_name:
            search_conditions.append(self.employee_model.first_name.contains(search_by_employee_first_name))
        if search_by_employee_last_name is not None and search_by_employee_last_name:
            search_conditions.append(self.employee_model.last_name.contains(search_by_employee_last_name))
        if search_by_employee_uuid is not None and search_by_employee_uuid:
            search_conditions.append(self.employee_model.uuid == search_by_employee_uuid)

        query = self.service_model.query.filter_by(status=True).outerjoin(self.employee_model).outerjoin(self.currency_model).filter(and_(*search_conditions)).order_by(self.service_model.created_at.desc())
        query_result = query.offset(offset).limit(int(page_size))
        result_count = query.count()
        result = self.schema.dump(query_result, many=True)
        return jsonify({"page_no": page_no, "page_size": page_size, "result_count": result_count, "transaction_list": result})

    def create_record(self, request: object) -> TransactionModel:
        record = self.service_model(**request.data)
        record.save()
        result = self.schema.dump(record)
        return jsonify({'transaction': result})

    def update_record(self, request: object, transaction_id: str) -> TransactionModel:
        data = request.get_json()
        transaction_record_from_db = self.service_model.query.filter_by(uuid=transaction_id).scalar()
        if transaction_record_from_db is None:
            return jsonify({"status": False, "message": "record not found"})

        if not isinstance(data["currency"], int):
            currency_record_from_db = CurrencyModel.query.filter(or_(CurrencyModel.id == data['currency']['id'],
                                                                 CurrencyModel.currency_code == data['currency']['currency_code'])).scalar()
        else:
            currency_record_from_db = CurrencyModel.query.filter(or_(CurrencyModel.id == data['currency'],
                                                                     CurrencyModel.currency_code == str(data['currency']))).scalar()
        if currency_record_from_db is not None:
            transaction_record_from_db.currency_id = currency_record_from_db.id

        transaction_record_from_db.description = data['description']
        transaction_record_from_db.amount = data['amount']
        transaction_record_from_db.approval_status = data['approval_status']
        transaction_record_from_db.commit()
        return jsonify({"status": True, "message":"record updated",'transaction': self.schema.dump(transaction_record_from_db)})

    def delete_record(self, request: object, transaction_id: str) -> TransactionModel:
        transaction_record_from_db = self.service_model.query.filter_by(uuid=transaction_id).scalar()

        if transaction_record_from_db is None:
            return jsonify({"status": False, "message": "record not found"})

        transaction_record_from_db.status = False
        transaction_record_from_db.commit()
        return jsonify(
            {"status": True, "message": "record deleted", 'transaction': self.schema.dump(transaction_record_from_db)})

    def get_analytics_record(self) -> object:
        current_time = datetime.datetime.utcnow().date()
        query_result = self.service_model.query.with_entities(self.service_model.approval_status, self.service_model.created_at).filter_by(status=True)
        pending_approval = query_result.filter_by(approval_status='pending').count()
        today_count = query_result.filter(self.service_model.created_at >= current_time).count()
        result_count = query_result.count()
        employee_query_result = self.employee_model.query.count()

        return jsonify({"result_count": result_count, "pending_approval": pending_approval, "today_count": today_count,
                        "employee_count": employee_query_result})

