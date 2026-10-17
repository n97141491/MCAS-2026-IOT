
import serial
import tm1637
import time

# TM1637 腳位設定（BCM）
CLK = 17
DIO = 27

display = tm1637.TM1637(clk=CLK, dio=DIO)
display.brightness(2)
display.show("0000")

# UART 通訊設定
uart = serial.Serial(
    port="/dev/serial0",
    baudrate=9600,
    timeout=2
)

try:
    print("Lab 4-3 UART 通訊測試")
    print("請確認 TXD 與 RXD 已連接")
    print("輸入 0~9999，輸入 q 結束")

    while True:
        message = input("請輸入數字: ").strip()

        if message.lower() == "q":
            break

        if not message.isdigit() or len(message) > 4:
            print("請輸入最多四位數字")
            continue

        # 清除先前的接收資料
        uart.reset_input_buffer()

        # UART 發送數字
        uart.write((message + "\n").encode("utf-8"))
        uart.flush()
        print("UART 發送:", message)

        # UART 接收資料
        received = uart.readline().decode(
            "utf-8", errors="replace"
        ).strip()

        if received:
            print("UART 接收:", received)

            if received.isdigit() and len(received) <= 4:
                display.show(received.zfill(4))
                print("TM1637 顯示:", received.zfill(4))
            else:
                print("收到的內容無法顯示在四位數顯示器")
        else:
            print("UART 接收逾時")

        time.sleep(0.5)

except KeyboardInterrupt:
    print("\n停止通訊")

finally:
    display.show("    ")
    uart.close()
    print("程式結束")
