import datetime as dt
import tkinter as tk
from time import sleep

import matplotlib.animation as animation
import matplotlib.pyplot as plt
import serial
import xlrd
import xlwt
from xlutils.copy import copy

list_in_floats = []
average_values = [[0.0, 0.0, 0.0] * 6]
pros1_temp = [0.0, 0.0, 0.0]
pros1_vlag = [0.0, 0.0, 0.0]
pros1_UV = [0.0, 0.0, 0.0]
pros2_temp = [0.0, 0.0, 0.0]
pros3_temp = [0.0, 0.0, 0.0]
pros4_temp = [0.0, 0.0, 0.0]
power_avg = [0.0, 0.0, 0.0]
current_avg = [0.0, 0.0, 0.0]
voltage_avg = [0.0, 0.0, 0.0]
counter = 0

counter2 = 0
counter1 = 2

xs = []
temp1 = []
temp2 = []
temp3 = []
temp4 = []
uv = []
humidity = []
power = []
current = []
voltage = []
col = 0
excel_lista = [["Vrijeme", "Temperatura1", "Temperatura2", "Temperatura3", "Temperatura4", "UV", "Humidity", "Voltage", "Current", "Power"]]
# Initialize communication with TMP102

rb = xlrd.open_workbook('Mjerenja.xls', formatting_info=True)
r_sheet = rb.sheet_by_index(0)
row = r_sheet.nrows
wb = copy(rb)
ws = wb.get_sheet(0)

# This function is called periodically from FuncAnimation
def animate(i, xs, temp1, temp2, temp3, temp4, uv, humidity, voltage, current, power):
    global counter2
    global counter1
    global row

    global workbook
    global worksheet
    counter2 = counter2 + 1
    counter1 = counter1 * 2
    vrijeme = (dt.datetime.now().strftime('%H:%M:%S'))
    # Read temperature (Celsius) from TMP102

    temp1_tmp = calculate_average(pros1_temp)
    temp2_tmp = calculate_average(pros2_temp)
    temp3_tmp = calculate_average(pros3_temp)
    temp4_tmp = calculate_average(pros4_temp)
    uv_tmp = calculate_average(pros1_UV)
    humidity_tmp = calculate_average(pros1_vlag)
    power_tmp = calculate_average(power_avg)
    current_tmp = calculate_average(current_avg)
    voltage_tmp = calculate_average(voltage_avg)

    ws.write(row, 0, vrijeme)
    ws.write(row, 1, temp1_tmp)
    ws.write(row, 2, temp2_tmp)
    ws.write(row, 3, temp3_tmp)
    ws.write(row, 4, temp4_tmp)
    ws.write(row, 5, uv_tmp)
    ws.write(row, 6, humidity_tmp)
    ws.write(row, 7, voltage_tmp)
    ws.write(row, 8, current_tmp)
    ws.write(row, 9, power_tmp)

    row = row + 1

    # Add x and y to lists
    xs.append(vrijeme)
    temp1.append(temp1_tmp)
    temp2.append(temp2_tmp)
    temp3.append(temp3_tmp)
    temp4.append(temp4_tmp)
    uv.append(uv_tmp)
    humidity.append(humidity_tmp)
    voltage.append(voltage_tmp)
    current.append(current_tmp)
    power.append(power_tmp)
    # Limit x and y lists to 20 items
    xs = xs[-20:]
    temp1 = temp1[-20:]
    temp2 = temp2[-20:]
    temp3 = temp3[-20:]
    temp4 = temp4[-20:]
    uv = uv[-20:]
    humidity = humidity[-20:]
    current = current[-20:]
    voltage = voltage[-20:]
    power = power[-20:]


    # Draw x and y lists
    ax[0, 0].clear()
    ax[0, 1].clear()
    ax[1, 0].clear()
    ax[2, 0].clear()
    ax[2, 1].clear()
    ax[1, 1].clear()
    ax[3, 0].clear()
    ax[3, 1].clear()
    ax[4, 0].clear()
    ax[0, 0].set_title("Temperature 1")
    ax[0, 0].plot(xs, temp1, color="blue")
    ax[0, 0].tick_params(axis='x', labelrotation=45)
    ax[0, 1].set_title("Temperature 2")
    ax[0, 1].plot(xs, temp2, color="blue")
    ax[1, 0].set_title("Temperature 3")
    ax[1, 0].plot(xs, temp3, color="blue")
    ax[1, 1].set_title("Temperature 4")
    ax[1, 1].plot(xs, temp4, color="blue")
    ax[2, 0].set_title("UV")
    ax[2, 0].plot(xs, uv, color="blue")
    ax[2, 1].set_title("Humidity")
    ax[2, 1].plot(xs, humidity, color="blue")
    ax[0, 1].tick_params(axis='x', labelrotation=45)
    ax[1, 0].tick_params(axis='x', labelrotation=45)
    ax[1, 1].tick_params(axis='x', labelrotation=45)
    ax[2, 0].tick_params(axis='x', labelrotation=45)
    ax[2, 1].tick_params(axis='x', labelrotation=45)
    ax[3, 0].tick_params(axis='x', labelrotation=45)
    ax[3, 1].tick_params(axis='x', labelrotation=45)
    ax[4, 0].tick_params(axis='x', labelrotation=45)
    ax[0, 0].set_ylabel("Temp (Celsius)")
    ax[0, 0].set_xlabel("Time")
    ax[0, 1].set_ylabel("Temp (Celsius)")
    ax[0, 1].set_xlabel("Time")
    ax[1, 0].set_ylabel("Temp (Celsius)")
    ax[1, 0].set_xlabel("Time")
    ax[1, 1].set_ylabel("Temp (Celsius)")
    ax[1, 1].set_xlabel("Time")
    ax[2, 0].set_ylabel("UV index")
    ax[2, 0].set_xlabel("Time")
    ax[2, 1].set_ylabel("Humidity (%)")
    ax[2, 1].set_xlabel("Time")
    ax[3, 0].set_title("Voltage")
    ax[3, 0].plot(xs, voltage, color="blue")
    ax[3, 0].set_xlabel("Time")
    ax[3, 0].set_ylabel("Voltage (V)")
    ax[3, 1].set_title("Current")
    ax[3, 1].plot(xs, current, color="blue")
    ax[3, 1].set_xlabel("Time")
    ax[3, 1].set_ylabel("Current (A)")
    ax[4, 0].set_title("Power")
    ax[4, 0].plot(xs, power, color="blue")
    ax[4, 0].set_xlabel("Time")
    ax[4, 0].set_ylabel("Power (W)")
    ax[4, 1].set_visible(False)


def toText(v):
    if str(v) == '1':
        return "ON"
    elif str(v) == '0':
        return "OFF"
    else:
        return str(v)

def add_new_values(values):
    global counter

    pros1_temp[counter] = 0.0 if (values[0] == '') else float(values[0])
    pros1_vlag[counter] = 0.0 if (values[1] == '') else float(values[1])
    pros1_UV[counter] = 0.0 if (values[2] == '') else float(values[2])
    pros2_temp[counter] = 0.0 if (values[3] == '') else float(values[3])
    pros3_temp[counter] = 0.0 if (values[4] == '') else float(values[4])
    pros4_temp[counter] = 0.0 if (values[5] == '') else float(values[5])
    voltage_avg[counter] = 0.0 if (values[11] == '') else float(values[11])
    current_avg[counter] = 0.0 if (values[12] == '') else float(values[12])
    power_avg[counter] = 0.0 if (values[13] == '') else float(values[13])

    counter = (counter + 1) % 3

def calculate_average(values):
    sum = 0
    i = 0
    for v in values:
        if v != 0.0:
            sum += v
            i += 1
    if (i > 0): return round(sum / i, 2)
    return 0

def counter_label(label1, label2, label3, label4, label5, label6, label7, label8, label9, label10, label11, label12, label13, label14):
    def count():
        arduino = serial.Serial('com6', 9600)
        print('Established serial connection to Arduino')
        arduino_data = arduino.readline()
        arduino.close()
        decoded_values = str(arduino_data[0:len(arduino_data)].decode("utf-8"))
        list_values = decoded_values.split('x')
        if len(list_values) == 15:
            add_new_values(list_values)
            label1.config(text="Prostorija1 : temp - " + str(calculate_average(pros1_temp)))
            label2.config(text="Prostorija1 : vlaga - " + str(calculate_average(pros1_vlag)))
            label3.config(text="Prostorija1 : UV - " + str(calculate_average(pros1_UV)))
            label4.config(text="Prostorija2 : temp - " + str(calculate_average(pros2_temp)))
            label5.config(text="Prostorija3 : temp - " + str(calculate_average(pros3_temp)))
            label6.config(text="Prostorija4 : temp - " + str(calculate_average(pros4_temp)))
            label7.config(text="Prostorija1 : grijac - " + toText(list_values[6]))
            label8.config(text="Prostorija2 : grijac - " + toText(list_values[7]))
            label9.config(text="Prostorija3 : grijac - " + toText(list_values[8]))
            label10.config(text="Prostorija4 : grijac - " + toText(list_values[9]))
            label11.config(text="Prostorija1 : LED - " + toText(list_values[10]))
            label12.config(text="Napon - " + ("Not available" if (int(list_values[11]) > 5000 or int(list_values[11]) < 0) else str(int(list_values[11])/1000) + " V"))
            label13.config(text="Struja - " + ("Not available" if (int(list_values[12]) > 20000 or int(list_values[12]) < 0) else str(int(list_values[12])/1000) + " A"))
            label14.config(text="Snaga - " + str(float("{:.3f}".format(int(list_values[11])/1000 * int(list_values[12])/1000))) + " W")

        list_values.clear()
        root.after(4000, count)
    count()


sleep(3)
root = tk.Tk()
root.geometry("230x650")
root.title("Values of sensors")

fig, ax = plt.subplots(5, 2)
fig.tight_layout(pad=2)

label1 = tk.Label(root, fg="green")
label1.pack(anchor="w", padx=(20, 10))
label2 = tk.Label(root, fg="green")
label2.pack(anchor="w", padx=(20, 10))
label3 = tk.Label(root, fg="green")
label3.pack(anchor="w", padx=(20, 10))
label4 = tk.Label(root, fg="green")
label4.pack(anchor="w", padx=(20, 10))
label5 = tk.Label(root, fg="green")
label5.pack(anchor="w", padx=(20, 10))
label6 = tk.Label(root, fg="green")
label6.pack(anchor="w", padx=(20, 10))
label7 = tk.Label(root, fg="green")
label7.pack(anchor="w", padx=(20, 10))
label8 = tk.Label(root, fg="green")
label8.pack(anchor="w", padx=(20, 10))
label9 = tk.Label(root, fg="green")
label9.pack(anchor="w", padx=(20, 10))
label10 = tk.Label(root, fg="green")
label10.pack(anchor="w", padx=(20, 10))
label11 = tk.Label(root, fg="green")
label11.pack(anchor="w", padx=(20, 10))
label12 = tk.Label(root, fg="green")
label12.pack(anchor="w", padx=(20, 10))
label13 = tk.Label(root, fg="green")
label13.pack(anchor="w", padx=(20, 10))
label14 = tk.Label(root, fg="green")
label14.pack(anchor="w", padx=(20, 10))
counter_label(label1, label2, label3, label4, label5, label6, label7, label8, label9, label10, label11, label12, label13, label14)
tb1 = tk.Text(
    root,
    height=1,
    width=10
)
tb2 = tk.Text(
    root,
    height=1,
    width=10
)
tb3 = tk.Text(
    root,
    height=1,
    width=10
)
tb4 = tk.Text(
    root,
    height=1,
    width=10
)
tb5 = tk.Text(
    root,
    height=1,
    width=10
)
label15 = tk.Label(text="Prva ref. temperatura")
label15.pack(anchor="w", padx=(20, 10))
tb1.pack(anchor="w", padx=(20, 10))
label16 = tk.Label(text="Druga ref. temperatura")
label16.pack(anchor="w", padx=(20, 10))
tb2.pack(anchor="w", padx=(20, 10))
label17 = tk.Label(text="Treca ref. temperatura")
label17.pack(anchor="w", padx=(20, 10))
tb3.pack(anchor="w", padx=(20, 10))
label18 = tk.Label(text="Cetvrta ref. temperatura")
label18.pack(anchor="w", padx=(20, 10))
tb4.pack(anchor="w", padx=(20, 10))
label19 = tk.Label(text="Peta ref. UV")
label19.pack(anchor="w", padx=(20, 10))
tb5.pack(anchor="w", padx=(20, 10))

def retrieve_input():
    inputValue = tb1.get("1.0","end-1c")
    inputValue += "-"
    inputValue += tb2.get("1.0","end-1c")
    inputValue += "-"
    inputValue += tb3.get("1.0", "end-1c")
    inputValue += "-"
    inputValue += tb4.get("1.0", "end-1c")
    inputValue += "-"
    inputValue += tb5.get("1.0", "end-1c")
    arduino2 = serial.Serial('com6', 9600)
    arduino2.write(inputValue.encode())
    print(inputValue)
label20 = tk.Label(text="")
label20.pack()
buttonCommit= tk.Button(root, height=1, width=25, text="Send", command=lambda: retrieve_input())
#command=lambda: retrieve_input() >>> just means do this when i press the button
buttonCommit.pack(anchor="w", padx=(20, 10))
label21 = tk.Label(text="")
label21.pack()
button = tk.Button(root, text='Exit', width=25, command=root.destroy)
button.pack(anchor="w", padx=(20, 10))

ani = animation.FuncAnimation(fig, animate, fargs=(xs, temp1, temp2, temp3, temp4, uv, humidity, voltage, current, power), interval=1000)
mng = plt.get_current_fig_manager()
mng.window.state('zoomed')
plt.show()
wb.save('Mjerenja.xls')

root.mainloop()
