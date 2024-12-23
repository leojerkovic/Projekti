#include <QApplication>
#include <QLabel>
#include <QMainWindow>
#include <QMessageBox>
#include <QMouseEvent>
#include <QAction>
#include <QMenu>
#include <QMenuBar>
#include <QPainter>
#include <QFileDialog>
#include <QTextStream>

class MyMainWindow : public QMainWindow {
private:
    int i;
    int j;
public:
    MyMainWindow();
    QLabel* MyLabel;
    void mousePressEvent(QMouseEvent *event) override;
    void paintEvent(QPaintEvent* event) override;
    void EditNoviOblikMenu();
    QMenu* EditMenu;
    QAction* EditNoviOblik;
    QVector<QPoint> points;
    QVector<QString> shapes={"Kvadrat","Trokut","Krug"};
    QVector<QString> ShapeOrder;
    QString current;
    QString prikaz;
    int setint();
    void FileSaveAsMenu();
    void FileOpenMenu();
    QMenu* FileMenu;
    QAction* FileSaveAs;
    QAction* FileOpen;
};

MyMainWindow::MyMainWindow() {
    i=0;
    j=0;
    current="Krug";
    prikaz="Oblik: " + current;
    MyLabel = new QLabel(this);
    MyLabel->setText(prikaz);
    MyLabel->move(10, 20);

    EditNoviOblik = new QAction(tr("&Drugi oblik..."), this);
    EditNoviOblik->setShortcut(tr("CTRL+D"));
    connect(EditNoviOblik, &QAction::triggered, this, &MyMainWindow::EditNoviOblikMenu);
    EditMenu = menuBar()->addMenu(tr("&Uredi"));
    EditMenu->addAction(EditNoviOblik);

    FileSaveAs = new QAction(tr("&Spremi kao..."), this);
    FileSaveAs->setShortcut(tr("CTRL+S"));
    connect(FileSaveAs, &QAction::triggered, this, &MyMainWindow::FileSaveAsMenu);

    FileOpen = new QAction(tr("&Otvori..."), this);
    FileOpen->setShortcut(tr("CTRL+O"));
    connect(FileOpen, &QAction::triggered, this, &MyMainWindow::FileOpenMenu);

    FileMenu = menuBar()->addMenu(tr("&Datoteka"));
    FileMenu->addAction(FileSaveAs);
    FileMenu->addAction(FileOpen);

}

void MyMainWindow::FileSaveAsMenu(){
    QString fileName = QFileDialog::getSaveFileName(this, "Spremi kao...", "", "OBLIK File (*.obl)");
    if (!fileName.isEmpty()) {
        QFile file(fileName);
        if (!file.open(QIODevice::WriteOnly)) {
            QMessageBox::information(this, "Nemoguce otvaranje datoteke", file.errorString());
            return;
        }
        QTextStream out(&file);
        int i=0;
        out << "oblik file" << Qt::endl;
        for(const QPoint &point:points){
            i++;
        }
        out << i << Qt::endl;
        for(const QPoint &point:points){
            out << point.x() << " " << point.y() << Qt::endl;
        }
        for(const QString &string:ShapeOrder){
            out << string << Qt::endl;
        }
        out << pos().x() << Qt::endl;
        out << pos().y() << Qt::endl;
        out << size().width() << Qt::endl;
        out << size().height() << Qt::endl;
    }
}

void MyMainWindow::FileOpenMenu(){
    QString fileName = QFileDialog::getOpenFileName(this, "Otvori oblike...", "", "OBLIK File (*.obl)");
    if (!fileName.isEmpty()) {
        QFile file(fileName);
        if (!file.open(QIODevice::ReadOnly)) {
            QMessageBox::information(this, "Nemoguce otvaranje datoteke", file.errorString());
            return;
        }
        int x,y,z,w;
        int br;
        points.clear();
        ShapeOrder.clear();
        QPoint tpoint;
        QTextStream in(&file);
        QString str; str = in.readLine();
        if(str=="oblik file") {
            in >> br;
            for(int i=0;i<br;i++){
                in >> x >> y;
                tpoint.setX(x);
                tpoint.setY(y);
                points.append(tpoint);
            }
            for(int i=0;i<br;i++){
                in >> str;
                ShapeOrder.append(str);
            }
            in >> x >> y >> z >> w;
            this->setGeometry(x, y, z, w);
        }
    }
}

int MyMainWindow::setint(){
    if(i==2) {
        i=0;
        return 2;
    }
    else {
        return i++;
    }
}
void MyMainWindow::EditNoviOblikMenu() {
    current=shapes[setint()];
    prikaz="Oblik: " + current;
    MyLabel->setText(prikaz);
}
void MyMainWindow::paintEvent(QPaintEvent*){
    QPainter painter(this);
    for (const QPoint &point : points) {
        if(ShapeOrder[j]=="Krug"){
            painter.drawEllipse(point, 25, 25);
        }
        else if (ShapeOrder[j]=="Kvadrat"){
            painter.drawLine(point.x(),point.y(),point.x()+35,point.y());
            painter.drawLine(point.x()+35,point.y(),point.x()+35,point.y()+35);
            painter.drawLine(point.x()+35,point.y()+35,point.x(),point.y()+35);
            painter.drawLine(point.x(),point.y()+35,point.x(),point.y());
        }
        else if (ShapeOrder[j]=="Trokut"){
            painter.drawLine(point.x(),point.y(),point.x()-25,point.y()+35);
            painter.drawLine(point.x()-25,point.y()+35,point.x()+25,point.y()+35);
            painter.drawLine(point.x()+25,point.y()+35,point.x(),point.y());
        }
        j++;
    }
    j=0;
}

void MyMainWindow::mousePressEvent(QMouseEvent* event) {
    if (event->button() == Qt::LeftButton) {
        points.append(event->pos());
        ShapeOrder.append(current);
        update();
    }
    else if(event->button() == Qt::RightButton){
        current=shapes[setint()];
        prikaz="Oblik: " + current;
        MyLabel->setText(prikaz);
    }
}
int main(int argc, char **argv) {
    QApplication app (argc, argv);
    MyMainWindow mainWindow;
    mainWindow.resize(720,480);
    mainWindow.show();
    return app.exec();
}
