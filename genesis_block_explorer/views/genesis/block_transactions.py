from pprint import pprint
from datetime import datetime, timezone

from flask import request
from flask import render_template, request, jsonify, current_app as app

from ...logging import get_logger
from datatables import ColumnDT, DataTables
from sqlalchemy.orm.exc import NoResultFound

from ...db import db

from ...models.genesis.explicit import BlockChain
from ...models.genesis.helpers import BlockTransactionsHelper
from ...models.db_engine.session import SessionManager
from ...models.genesis.utils import get_by_id_or_first_genesis_db_id

from ...datatables import DataTablesExt

logger = get_logger(app)
sm = SessionManager(app=app)

class DataTablesBlockTransactionsHelper(DataTablesExt):
    pass

@app.route('/dt/genesis/database/<int:id>/block-transactions/<int:block_id>')
def block_transactions(id, block_id):
    show_raw_data = request.args.get("show_raw_data", False)
    if show_raw_data == "False":
        show_raw_data = False
    model = BlockTransactionsHelper
    column_ids = ['time', 'type', 'key_id', 'hash', 'contract_name', 'params']
    columns = [getattr(model, col_id) for col_id in column_ids]
    dt_columns = [ColumnDT(m) for m in columns]
    BlockTransactionsHelper.update_from_block(db_id=id, block_id=block_id,                                                    show_raw_data=show_raw_data)
    query = db.session.query(*columns).filter_by(db_id=id, block_id=block_id)
    params = request.args.to_dict()
    rowTable = DataTablesBlockTransactionsHelper(params, query, dt_columns)
    return jsonify(rowTable.output_result())
