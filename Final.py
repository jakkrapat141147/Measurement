import machine
import time

# ตั้งค่าขา ADC ที่ต่อกับวงจร (GP26)
adc = machine.ADC(machine.Pin(26))

# สร้างไฟล์ CSV ในตัวบอร์ดเพื่อเก็บข้อมูล
file = open("temperature_log.csv", "w")
file.write("Time(s),Raw_ADC,Voltage(V),Temp(C)\n")

print("--- เริ่มอ่านค่าอุณหภูมิจริง (ล็อคช่วง 20-50 C) ---")
print("หากต้องการหยุด ให้กดปุ่ม Stop (สีแดง) ด้านบนของ Thonny")
print("-" * 55)
print("Time(s) | Raw ADC | Voltage(V) | Temp(C)")

start_time = time.time()

try:
    while True:
        # 1. อ่านค่าดิบ
        raw_adc = adc.read_u16()
        
        # 2. คำนวณเป็นแรงดันไฟฟ้า (V)
        voltage = (raw_adc * 3.3) / 65535
        
        # 3. แปลงแรงดันเป็นอุณหภูมิ (จากสมการล่าสุดของคุณ)
        temp_c = (14.25 * voltage) + 5.84
        
        # --- เพิ่มส่วนการล็อคค่า (Clamping) ตามที่คุณต้องการ ---
        if temp_c < 20.0:
            temp_c = 20.0
        elif temp_c > 50.0:
            temp_c = 50.0
        # -----------------------------------------------
            
        # 4. เวลาที่ผ่านไป
        current_time = time.time() - start_time
        
        # 5. แสดงผลบนจอ
        print("{:7.1f} | {:7d} | {:.4f} V   | {:.2f} °C".format(current_time, raw_adc, voltage, temp_c))
        
        # 6. บันทึกลงไฟล์
        file.write("{:.1f},{},{:.4f},{:.2f}\n".format(current_time, raw_adc, voltage, temp_c))
        file.flush()
        
        time.sleep(1)

except KeyboardInterrupt:
    file.close()
    print("-" * 55)
    print("บันทึกไฟล์เสร็จสิ้น!")