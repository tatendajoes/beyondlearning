import dash
from dash import dcc, html, dash_table, Input, Output, State
import dash_bootstrap_components as dbc
import dash_ag_grid as dag
from dash_extensions.javascript import assign
from flask_socketio import SocketIO
import pandas as pd
from deps.datastore import ClassRecord
from datetime import date, datetime

database = ClassRecord('sqlite:///database.db')
database.initialize_db()

# -------------- Layout functions -------------------------------------------------
def page_classes():
    return dbc.Container(
        [
            # ---------- form card ----------
            dbc.Card(
                dbc.CardBody(
                    [
                        html.H2("Add a Class", className="mb-4"),
                        dbc.Input(id="cid",   placeholder="Class ID",    className="mb-2"),
                        dbc.Input(id="cname1", placeholder="Class Name",  className="mb-2"),
                        dbc.Input(id="clevel",placeholder="Class Level", type="number", className="mb-2"),
                        dbc.Input(id="cname2", placeholder="Instructor Name", className="mb-2"),
                        dbc.Button("Submit", id="submit", color="primary"),
                        html.Small(id="msg", className="ms-3 text-success"),
                    ]
                ),
                className="mb-4 shadow-sm",
            ),

            # ---------- table card ----------
# ---------- table card ----------
dbc.Card(
    dbc.CardBody(
        [
            html.H3("Current Classes", className="mb-3"),

            # custom JS to build a context menu
            # ↓ assign() tells Dash this is literal JS, not a Python string
            html.Div(id="delete-sentinel", style={"display": "none"}),  # dummy target

            dag.AgGrid(
                id="table",
                columnDefs=[
                    {"headerName": "ID",         "field": "class_id"},
                    {"headerName": "Name",       "field": "class_name"},
                    {"headerName": "Level",      "field": "class_level"},
                    {"headerName": "Instructor", "field": "instructor_name"},
                    {"headerName": "HasSession", "field": "has_session", "hide": True},
                ],
                rowData=database.fetch_all(1).to_dict("records"),
                defaultColDef={"resizable": True},
                dashGridOptions={
                    # JS function that returns the context-menu items
                    "getContextMenuItems": assign(
                        """
                        function(params){
                            const std = ['copy', 'paste'];
                            const canDelete = !params.node.data.has_session;
                            const del = {
                                name: 'Delete row',
                                disabled: !canDelete,
                                action: () => {
                                    // Push class_id into a hidden div so Dash picks it up
                                    document.getElementById('delete-sentinel')
                                            .setAttribute('data-cid', params.node.data.class_id);
                                }
                            };
                            return std.concat(['separator', del]);
                        }
                        """
                    )
                },
                style={"height": "500px", "width": "100%"},
            ),
        ]
    ),
    className="shadow-sm",
)
,
        ],
        fluid=True,
    )

# --- sessions page ---
def page_sessions():
    classes_df = database.fetch_all(1)
    return dbc.Container(
        [
            html.H2("Sessions", className="mb-3"),

            dbc.Button(" New Session", id="start-rec", color="primary", className="mb-3"),

            # ── form ───────────────────────────────────────────────
            dbc.Collapse(
                dbc.Card(
                    dbc.CardBody(
                        [
                            dbc.Input(id="s-desc",  placeholder="Session description", className="mb-2"),
                            dcc.DatePickerSingle(id="s-date", className="mb-2"),
                            dbc.Input(id="s-start", placeholder="Start time (HH:MM)", type="time", className="mb-2"),
                            dbc.Input(id="s-end",   placeholder="End time (HH:MM)",   type="time", className="mb-2"),
                            dbc.Input(id="s-att",   placeholder="Attendance",          type="number", className="mb-2"),
                            dbc.Select(
                                id="s-class", className="mb-3",
                                options=[
                                    {"label": f"{row.class_name} ({row.class_id})", "value": row.class_id}
                                    for row in classes_df.itertuples()
                                ],
                                placeholder="Select class",
                            ),
                             dbc.Row([
                            dbc.Col(
                                dbc.Button("Start Record", id="record-toggle-btn", color="danger", className="me-2"),
                                width="auto"
                            ),
                            dbc.Col(html.Div(id="record-status"), width="auto"),
                        ], className="mb-3"),
                            dbc.Button("Save", id="save-session", color="primary", disabled=True),
                            html.Small(id="s-msg", className="ms-3 text-success"),
                        ]
                    )
                ),
                id="session-form",
                is_open=False,
            ),

            # ── grid of existing sessions ──────────────────────────
            dag.AgGrid(
                id="sessions-grid",
                columnDefs=[
                    {"headerName": "ID",      "field": "session_id", "width": 220},
                    {"headerName": "ClassID", "field": "class_id"},
                    {"headerName": "Date",    "field": "date"},
                    {"headerName": "Start",   "field": "start_time"},
                    {"headerName": "End",     "field": "end_time"},
                    {"headerName": "Attend.", "field": "attendance"},
                    {"headerName": "Desc.",   "field": "description", "flex": 1},
                ],
                rowData=database.fetch_all(2).to_dict("records"),
                defaultColDef={"resizable": True},
                style={"height": "400px"},
            ),
        ],
        fluid=True,
    )


def page_metrics():
    return dbc.Container(
        dbc.Alert("Metrics page — build me next!", color="secondary"),
        fluid=True,
    )

# ─── router ---------------------------------------------------------------------
def router(path):
    return {"/sessions": page_sessions,
            "/metrics":  page_metrics}.get(path, page_classes)()

# ─── app shell ------------------------------------------------------------------
app = dash.Dash(
    __name__,
    title="Beyond Learning",
    external_stylesheets=[
        dbc.themes.FLATLY,
        "https://cdn.jsdelivr.net/npm/bootstrap-icons@1.11.3/font/bootstrap-icons.css",
    ],
    suppress_callback_exceptions=True,
)

socketio = SocketIO(app.server, async_mode='eventlet', cors_allowed_origins="*")

NAVBAR = dbc.NavbarSimple(
    brand="Beyond Learning",
    brand_style={"fontWeight": "600", "fontSize": "1.5rem"},
    color="primary",
    dark=True,
    fluid=True,
)

SIDEBAR = dbc.Nav(
    [
        dbc.NavLink([html.I(className="bi bi-journal-text me-2"), "Classes"],
                    href="/classes",  id="nav-classes",  active="exact"),
        dbc.NavLink([html.I(className="bi bi-calendar-event me-2"), "Sessions"],
                    href="/sessions", id="nav-sessions", active="exact"),
        dbc.NavLink([html.I(className="bi bi-bar-chart me-2"), "Metrics"],
                    href="/metrics",  id="nav-metrics",  active="exact"),
    ],
    vertical=True, pills=True,
    className="bg-light border-end vh-100 pt-4",
)

app.layout = html.Div(
    [
        dcc.Location(id="url"),
        NAVBAR,
        dbc.Container(
            dbc.Row(
                [
                    dbc.Col(SIDEBAR, width=2),
                    dbc.Col(html.Div(id="page-content", className="p-4"), width=10),
                ],
                className="g-0",
            ),
            fluid=True,
        ),
    ]
)

# ─── callbacks ------------------------------------------------------------------
@app.callback(
    Output("table", "rowData", allow_duplicate=True),
    Input("delete-sentinel", "data-cid"),          # fires when the JS sets data-cid
    prevent_initial_call=True,
)
def delete_row(cid):
    if cid:
        database.delete_row(cid)                   # remove from DB
    return database.fetch_all(1).to_dict("records") # reload grid

@app.callback(Output("page-content", "children"),
              Input("url", "pathname"))
def display_page(path):
    return router(path)

@app.callback(
    [
        Output("msg", "children"),
        Output("table", "rowData"),
        Output("cid", "value"),
        Output("cname1", "value"),
        Output("clevel", "value"),
        Output("cname2", "value"),
    ],
    Input("submit", "n_clicks"),
    [
        State("cid", "value"),
        State("cname1", "value"),
        State("clevel", "value"),
        State("cname2", "value"),
    ],
    prevent_initial_call=True,
)
def save(n, cid, cname1, clevel, cname2):
    if not (cid and cname1 and clevel and cname2):
        return "⛔ All fields required.", dash.no_update, *[dash.no_update]*4
    try:
        database.insert_row(
            cid.strip(),
            cname1.strip(),
            clevel,
            cname2.strip(),
            has_session=False,          # stays False until Session page sets it True
        )
        df = database.fetch_all(1)
        return "✅ Saved!", df.to_dict("records"), "", "", "", ""
    except ValueError:
        return "⛔ Use HH:MM.", dash.no_update, *[dash.no_update]*4

# --- open the form and pre-fill date/start time -----------------------

@app.callback(
    Output("session-form", "is_open"),
    Output("s-date", "date"),
    Output("s-start", "value"),
    Input("start-rec", "n_clicks"),
    prevent_initial_call=True,
)
def open_form(n):
    now = datetime.now()
    return True, now.date(), now.strftime("%H:%M")

# --- open / close the form and (only when opening) pre‑fill date & start ----

# --- save session -----------------------------------------------------
@app.callback(
    Output("s-msg", "children"),
    Output("sessions-grid", "rowData", allow_duplicate=True),
    Output("s-desc",  "value"),
    Output("s-date",  "date",  allow_duplicate=True),  
    Output("s-start", "value", allow_duplicate=True),   
    Output("s-end",   "value"),
    Output("s-att",   "value"),
    Output("s-class", "value"),
    Input("save-session", "n_clicks"),
    State("s-desc",  "value"),
    State("s-date",  "date"),
    State("s-start", "value"),
    State("s-end",   "value"),
    State("s-att",   "value"),
    State("s-class", "value"),
    prevent_initial_call=True,
)
def save_session(n, desc, d, t_start, t_end, att, cid):
    if not all([desc, d, t_start, t_end, att, cid]):
        return "⛔ fill every field", dash.no_update, *[dash.no_update]*6
    database.insert_session(
        class_id=cid,
        description=desc,
        date=d,
        start_time=t_start,
        end_time=t_end,
        attendance=int(att),
    )
    df = database.fetch_all(2)
    return "✅ saved", df.to_dict("records"), "", None, None, None, None, None

is_recording = False
@app.callback(
    Output("record-status", "children"),
    Output("record-toggle-btn", "children", allow_duplicate=True),
    Output("save-session", "disabled", allow_duplicate=True),
    Input("record-toggle-btn", "n_clicks"),
    prevent_initial_call=True
)
def toggle(n):
    global is_recording
    if not is_recording:
        socketio.emit('record', {'action': 'start'})
        is_recording = True
        return "⏺ Recording started", "Stop Record", False
    else:
        socketio.emit('record', {'action': 'stop'})
        is_recording = False
        return "⏹ Recording stopped" , "Start Record", True

# ─── run ------------------------------------------------------------------------
if __name__ == "__main__":
    #app.run(debug=False)
    socketio.run(app.server, host="0.0.0.0", port=8050, debug=True)
