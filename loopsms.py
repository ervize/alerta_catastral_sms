from threading import Timer
import time
import sms 


import mysql.connector


class RepeatTimer(Timer):
    def run(self):
        while not self.finished.wait(self.interval):
            self.function(*self.args, **self.kwargs)


mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="server2006",
  database="alerta_catastral"
)

def enviarmensajes(msg="foo"):
    print('Volvio a enviar')

    cur = mydb.cursor()
    cur.execute("SELECT * FROM mensajes WHERE estenviosms='N' LIMIT 1")
    result = cur.fetchall()
    print('Entrando a enviar')
    print(result)
    mydb.commit()

    for r in result:
        print('Entró')
        print(r[10])
        print(r[12])
        print(r[0])
        mensaje(r[10], r[12] + ' ' + r[1])
        print('Actualizando tabla mensajes')
        print ("UPDATE mensajes SET estenviosms='S' WHERE codmensaje='" + r[0]+"'")
        cur.execute("UPDATE mensajes SET estenviosms='S' WHERE codmensaje='" + r[0]+"'")
        mydb.commit()
    cur.close()

def mensaje(numcelular, mensaje):
    try:
            lsms = sms.TextMessage(numcelular , mensaje)
            lsms.connectPhone()
            lsms.sendMessage()
            lsms.disconnectPhone()
            print('Mensaje enviado correctamente')
    except:
            print('Error enviando mensaje')

# enviarmensajes()

timer = RepeatTimer(10, enviarmensajes)
timer.start()
time.sleep(86400)
timer.cancel()