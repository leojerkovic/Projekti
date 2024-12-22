#include <QApplication>
#include <QLabel>
#include <QMainWindow>
#include <QMessageBox>
#include <QMouseEvent>
#include <QAction>
#include <QMenu>
#include <QMenuBar>
#include <QPainter>

class MyMainWindow : public QMainWindow {
public:
    MyMainWindow();
    QLabel* MyLabel;
    void mousePressEvent(QMouseEvent *event) override;
    void paintEvent(QPaintEvent* event) override;
    void EditNoviOblikMenu();
    QMenu* EditMenu;
    QAction* EditNoviOblik;
};

MyMainWindow::MyMainWindow() {
    MyLabel = new QLabel(this);
    MyLabel->setText("Hello World!");
    MyLabel->move(10, 20);
    EditNoviOblik = new QAction(tr("&Drugi oblik..."), this);
    EditNoviOblik->setShortcut(tr("CTRL+D"));
    connect(EditNoviOblik, &QAction::triggered, this, &MyMainWindow::EditNoviOblikMenu);
    EditMenu = menuBar()->addMenu(tr("&Edit"));
    EditMenu->addAction(EditNoviOblik);

}
void MyMainWindow::EditNoviOblikMenu() {

}
void MyMainWindow::paintEvent(QPaintEvent*){
    //QSize size = this->size();
    QPainter painter(this);
    painter.drawLine(150, 100, 100, 200);
    painter.drawLine(100, 200, 200, 200);
    painter.drawLine(150, 100, 200, 200);
}

void MyMainWindow::mousePressEvent(QMouseEvent* event) {
    if (event->button() == Qt::LeftButton) {
        MyLabel->move(int(event->position().x()),int(event->position().y()));
    }
}
int main(int argc, char **argv) {
    QApplication app (argc, argv);
    MyMainWindow mainWindow;
    mainWindow.resize(300,150);
    mainWindow.show();
    return app.exec();
}