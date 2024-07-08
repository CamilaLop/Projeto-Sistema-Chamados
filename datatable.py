
from flet import *
import sqlite3

conn=sqlite3.connect('db/dbcad.db', check_same_thread=False)

tb=DataTable(
    columns=[
        DataColumn(Text('Ação')),
        DataColumn(Text('Título')),
        DataColumn(Text('Número')),
        DataColumn(Text('Responsável')),
        DataColumn(Text('Data')),
        DataColumn(Text('Transportadora (em caso de coleta)')),
        DataColumn(Text('Natureza')),
    ],
    rows=[]
)

def showdelete(e):
    try:
        myid = int(e.control.data)
        c = conn.cursor()
        c.execute("DELETE FROM users WHERE id=?",(myid,))
        conn.commit()
        tb.rows.clear()
        calldb()
        tb.update()

    except Exception as erro:
        print(erro)

id_edit = Text()
title_edit = TextField(label='Título')
number_edit = TextField(label='Número')
name_edit = TextField(label='Responsável')
nature_edit = RadioGroup(content=Column([
    Radio(value='Pagamento', label='Pagamento'),
    Radio(value='Coleta', label='Coleta'),
    Radio(value='Triangulação', label='Triangulação'),
    Radio(value='Divergência', label='Divergência')
]))
date_edit = TextField(label='Data')
carrier_edit = TextField(label='Transportadora (em caso de coleta)')

def hidedlg(e):
    dlg.visible=False
    dlg.update()

def updateandsave(e):
    try:
        myid = id_edit.value
        c=conn.cursor()
        c.execute(
            """UPDATE users SET title=?, name=?,
            number=?, nature=?, date=?, carrier=?
            WHERE id=?""", (title_edit.value, name_edit.value, 
            number_edit.value, nature_edit.value, date_edit.value, carrier_edit.value, myid)
        )
        conn.commit()
        print('Editados com sucesso')
        tb.rows.clear()
        calldb()
        dlg.visible=False
        dlg.update()
        tb.update()

    except Exception as erro:
        print('o erro está aqui', erro)

dlg = Container(
    bgcolor='green200',
    padding=10,
    content=Column([
        Row([
            Text(
                'Editar dados',
                size=20,
                weight='bold'
            ),
            IconButton(
                icon='close', 
                on_click=hidedlg
            )], alignment='spaceBetween'),
        title_edit,
        number_edit,
        name_edit,
        Text('Selecione a natureza', size=20,weight='bold'),
        nature_edit,
        date_edit,
        carrier_edit,
        ElevatedButton(
            'Atualizar',
            on_click=updateandsave
        ),
    ])
)

def showedit(e):
    data_edit = e.control.data
    id_edit.value = data_edit['id']
    title_edit.value = data_edit['title']
    number_edit.value = data_edit['number']
    name_edit.value = data_edit['name']
    nature_edit.value = data_edit['nature']
    date_edit.value = data_edit['date']
    carrier_edit.value = data_edit['carrier']

    dlg.visible=True
    dlg.update()

def calldb():
    c = conn.cursor()
    c.execute('SELECT * FROM users')
    users = c.fetchall()
    print(users)

    if not users == '':
        keys= ['id', 'title', 'name', 'number', 'nature', 'date', 'carrier']
        result = [dict(zip(keys, values)) for values in users]
        for x in result:
            tb.rows.append(
                DataRow(
                    cells=[
                        DataCell(
                            Row([
                                IconButton(
                                    icon='create',
                                    icon_color='blue',
                                    data=x,
                                    on_click=showedit
                                ),
                                IconButton(
                                    icon='delete',
                                    icon_color='red',
                                    data=x['id'],
                                    on_click=showdelete
                                ),
                            ])
                        ),
                        DataCell(Text(x['title'])),
                        DataCell(Text(x['number'])),
                        DataCell(Text(x['name'])),
                        DataCell(Text(x['date'])),
                        DataCell(Text(x['carrier'])),
                        DataCell(Text(x['nature'])),
                    ],
                ),
            )

calldb()
dlg.visible=False

mytable = Column([
    dlg,
    Row([tb],scroll='always')
])
