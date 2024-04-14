from models import Order, Employee
from operations import createSmena, getEmployees,\
makeAuth, getRoleById, getSmenaDataAll, getOrdersDataAll,\
deleteEmployeeById,\
getOrderById, changeStatusByOrderIdAndStatusId,\
createEmployee, createOrder, getLastSmena
from ui import InputDialogAddSmena, Ui_MainWindow,\
InputDialogAddEmployee, InputDialogAddOrder

class CurrnetEmployee:
    currnetEmployee: Employee = None

    
def auth(ui: Ui_MainWindow, login, password):
    employee = makeAuth(login, password)
    if (employee == None) or (employee.uvolen == True):
        ui.showErrorDialog(
            "Ошибка",
            "Логин или Пароль введены неправильно",
        )
        return
    
    CurrnetEmployee.currnetEmployee = employee
    if CurrnetEmployee.currnetEmployee.role == 1:
        ui.tabWidgetMainPage.setCurrentIndex(0)
        ui.pushButtonCreateOrder.setVisible(False)
        ui.pushButtonChangeStatus.setVisible(False)
        fillSmenaTable(ui)
        fillEmployeesTable(ui)
        
        fillOrderTable(ui, 100)

    elif CurrnetEmployee.currnetEmployee.role == 2:
        ui.tabWidgetMainPage.setCurrentIndex(1)
        ui.tabWidgetMainPage.setTabVisible(0, False)
        ui.tabWidgetMainPage.setTabVisible(2, False)
        
        fillOrderTable(ui, 1)

    elif CurrnetEmployee.currnetEmployee.role == 3:
        ui.tabWidgetMainPage.setCurrentIndex(1)
        ui.tabWidgetMainPage.setTabVisible(0, False)
        ui.tabWidgetMainPage.setTabVisible(2, False)
        ui.pushButtonCreateOrder.setVisible(False)
        fillOrderTable(ui, 1)

    
    
    
    role = getRoleById(CurrnetEmployee.currnetEmployee.role)
    ui.labelMainPageTitle.setText(role.role) 
    ui.stackedWidget.setCurrentIndex(1)

def addEmployee(ui: Ui_MainWindow):
    dialog: InputDialogAddEmployee = ui.showInputDialogAddEmployee()
    dialog.accepted.connect(lambda: buttonAddEmployeeProcess(ui=ui, dialog=dialog))
    dialog.exec()

def buttonAddEmployeeProcess(ui: Ui_MainWindow, dialog: InputDialogAddEmployee):
    name = dialog.lineEditName.text()
    secondName = dialog.lineEditSecondName.text()
    role = dialog.comboBoxRole.currentData()
    login = dialog.lineEditLogin.text()
    password = dialog.lineEditPassword.text()
    if (
        name == '' or
        secondName == '' or
        login == '' or
        password == ''
    ):
        ui.showErrorDialog('Ошибка', 'Нужно заполнить все поля!')
    else:
        createEmployee(name, secondName, role, login, password)
        fillEmployeesTable(ui)

def addOrder(ui: Ui_MainWindow):
    dialog: InputDialogAddOrder = ui.showInputDialogAddOrder()
    dialog.accepted.connect(lambda: buttonAddOrderProcess(ui=ui, dialog=dialog))
    dialog.exec()

def buttonAddOrderProcess(ui: Ui_MainWindow, dialog: InputDialogAddOrder):
    table = dialog.lineEditTable.text()
    countClients = dialog.lineEditCountClient.text()
    drinks = dialog.lineEditDrinks.text()
    dishes = dialog.lineEditDishes.text()
    smena = getLastSmena(CurrnetEmployee.currnetEmployee)
    if (
        table == '' or
        countClients == '' or
        drinks == '' or
        dishes == '' or 
        len(smena) == 0
        
    ):
        ui.showErrorDialog('Ошибка', 'Нужно заполнить все поля!')
    else:
        createOrder(table, countClients, drinks, dishes, smena[0])
        fillOrderTable(ui, 1)
    

def changeStatus(ui: Ui_MainWindow):
    if len(ui.tableWidgetOrders.selectedIndexes()) != 0:
        selectedOrderIndex = list(set(index.row() for index in
            ui.tableWidgetOrders.selectedIndexes()))[0]
        id = int(ui.tableWidgetOrders.item(selectedOrderIndex, 2).text())
        order: Order = getOrderById(id)
        if CurrnetEmployee.currnetEmployee.role == 2 and order.status == 4:
            changeStatusByOrderIdAndStatusId(id, 2)
        elif CurrnetEmployee.currnetEmployee.role == 3:
            if order.status == 1:
                changeStatusByOrderIdAndStatusId(id, 3)
            elif order.status == 3:
                changeStatusByOrderIdAndStatusId(id, 4)
            else:
                ui.showErrorDialog(
                "Ошибка",
                "Вы не можете изменить статус",
            )
        else:
            ui.showErrorDialog(
            "Ошибка",
            "Вы не можете изменить статус",
        )
        fillOrderTable(ui, 1)
    else: ui.showErrorDialog(
        "Ошибка",
        "Заказ не выбран",
    )

def deleteEmployee(ui: Ui_MainWindow):
    if len(ui.tableWidgetEmployees.selectedIndexes()) != 0:
        selectedEmployeeIndex = list(set(index.row() for index in
            ui.tableWidgetEmployees.selectedIndexes()))[0]
        
        id = int(ui.tableWidgetEmployees.item(selectedEmployeeIndex, 0).text())
        deleteEmployeeById(id)
        fillEmployeesTable(ui)
    else: ui.showErrorDialog(
        "Ошибка",
        "Сотрудник не выбран",
    )

def fillSmenaTable(ui: Ui_MainWindow):
    smenyWithEmployees = getSmenaDataAll()
    ui.fillSmenaTableWidget(smenyWithEmployees)

def fillOrderTable(ui: Ui_MainWindow, limit):
    smenyWithOrders = getOrdersDataAll(limit, CurrnetEmployee.currnetEmployee)
    ui.fillOrderTableWidget(smenyWithOrders)

def fillEmployeesTable(ui: Ui_MainWindow):
    employees = getEmployees()
    ui.fillEmployeesTableWidget(employees)


def addSmena(ui: Ui_MainWindow):
    employees = getEmployees()
    dialog: InputDialogAddSmena = ui.showInputDialogAddSmena(employees)
    dialog.accepted.connect(lambda: addSmenaButtonOkProcess(ui, dialog))
    dialog.exec()

def addSmenaButtonOkProcess(ui: Ui_MainWindow, dialog: InputDialogAddSmena):
    selectedRowsIndexes = set(index.row() for index in
        dialog.employeesTable.selectedIndexes())
    selectedEmployesIds = [dialog.employeesTable.item(i, 0).text() for i in selectedRowsIndexes]
    if len(selectedEmployesIds) == 0:
        ui.showErrorDialog('Ошибка', 'Смена не может быть без сотрудников')
    else:
        createSmena(selectedEmployesIds)
        fillSmenaTable(ui)

def logOut(ui: Ui_MainWindow):
    ui.stackedWidget.setCurrentIndex(0)
    ui.lineEditPassword.setText('')
    ui.lineEditLogin.setText('')
    ui.tabWidgetMainPage.setTabVisible(0, True)
    ui.tabWidgetMainPage.setTabVisible(1, True)
    ui.tabWidgetMainPage.setTabVisible(2, True)
    ui.pushButtonCreateOrder.setVisible(True)
    ui.pushButtonChangeStatus.setVisible(True)

def applyLogic(ui: Ui_MainWindow):
    CurrnetEmployee.currnetEmployee = None
    ui.pushButtonLogOut.clicked.connect(
        lambda: logOut(ui=ui)
    )
    ui.pushButtonAddSmena.clicked.connect(lambda: addSmena(
        ui=ui,
    ))
    ui.pushButtonDeleteEmployee.clicked.connect(
        lambda: deleteEmployee(ui)
    )
    ui.pushButtonAddEmployee.clicked.connect(
        lambda: addEmployee(ui)
    )
    ui.pushButtonEntry.clicked.connect(lambda: auth(
        ui=ui,
        login=ui.lineEditLogin.text(),
        password=ui.lineEditPassword.text(),
    ))
    ui.pushButtonChangeStatus.clicked.connect(
        lambda: changeStatus(ui)
    )
    ui.pushButtonCreateOrder.clicked.connect(
        lambda: addOrder(ui=ui)
    )
    ui.pushButtonUpdate.clicked.connect(
        lambda: updateAll(ui)
    )

def updateAll(ui: Ui_MainWindow):
    if CurrnetEmployee.currnetEmployee.role == 1:
        fillEmployeesTable(ui)
        fillSmenaTable(ui)
        fillOrderTable(ui, 100)
    else:
        fillOrderTable(ui, 1)
    
    

