import tkinter as tk
from tkinter import messagebox
from tkinter import font
#from pymodbus.client.sync import ModbusTcpClient #모두버스 설정
import threading

class ControlProgram:
    def __init__(self, root):
        self.root = root
        self.root.title("Control Program")
        
        # 윈도우 사이즈 조정 (기본적으로 두 배로 설정)
        self.root.geometry("600x400")  # 너비 600, 높이 400
        
        # 두 배 크기의 폰트 설정
        large_font = font.Font(size=20)  # 기본 폰트의 두 배 크기
        
        # Command list loaded from a file (with cp949 encoding)
        try:
            with open('commands.txt', 'r', encoding='cp949') as file:
                self.commands = file.read().splitlines()  # Read command list from file
        except Exception as e:
            messagebox.showerror("Error", f"Error occurred while reading the file: {e}")
            self.commands = []

        self.current_command_index = 0

        #모두버스 설정
        # Create MODBUS client to connect to the robot
        #self.client = ModbusTcpClient('localhost')  # IP address of the robot
        #self.client = ModbusTcpClient('192.168.0.10')  # IP address of the robot

        # Create UI elements with larger font
        self.command_label = tk.Label(root, text="Command List:", font=large_font)
        self.command_label.pack(pady=10)

        # Display command list (increase width and height)
        self.command_listbox = tk.Listbox(root, font=large_font, height=10, width=40)
        for command in self.commands:
            self.command_listbox.insert(tk.END, command)
        self.command_listbox.pack(pady=10)
        
        # Command execution button with larger size
        self.execute_button = tk.Button(root, text="Start", font=large_font, width=20, height=2, command=self.execute_command)
        self.execute_button.pack(pady=10)
        
        # Completion status label with larger font
        self.status_label = tk.Label(root, text="Status: Waiting", font=large_font)
        self.status_label.pack(pady=10)

    # Command execution function (in a separate thread)
    def execute_command(self):
        if self.current_command_index < len(self.commands):
            current_command = self.commands[self.current_command_index]
            self.status_label.config(text=f"Status: Executing '{current_command}'...")

            #모두버스 설정
            # Run the MODBUS command in a separate thread to avoid freezing the UI
            threading.Thread(target=self.send_modbus_command, args=(current_command,)).start()

        else:
            messagebox.showinfo("Info", "All commands have been executed.")

    # Send MODBUS command to the robot and process the response
    def send_modbus_command(self, command):
        try:
            
            #모두버스 설정
            # Simulating sending a command through MODBUS (use proper addresses and values)
            #self.client.connect()
            #result = self.client.write_coil(1, True)  # Example command; modify as needed
            #self.client.close()
            
           
            # Process the result and update the UI with the response
            #self.root.after(0, self.complete_command, result)
            
            # 테스트 Simulate command execution with a 2-second delay
            result = "Completed!"
            self.root.after(2000, self.complete_command, result)  # Complete after 2 seconds

        except Exception as e:
            self.root.after(0, self.update_status_error, str(e))

    # Update status when MODBUS command is completed
    def complete_command(self, result):
        current_command = self.commands[self.current_command_index]
        
        # Assuming result indicates success if no errors (you can parse the actual result)
        #if result.isError():
        completed_command = f"{current_command} - completed"
        #else:
         #   completed_command = f"{current_command} - completed"

        # Update the command list item to indicate completion
        self.command_listbox.delete(self.current_command_index)
        self.command_listbox.insert(self.current_command_index, completed_command)

        # Move to the next command
        self.current_command_index += 1
        if self.current_command_index < len(self.commands):
            self.command_listbox.selection_clear(0, tk.END)
            self.command_listbox.selection_set(self.current_command_index)
            self.execute_button.config(text="Execute Next Command")
        else:
            self.execute_button.config(state=tk.DISABLED)

        self.status_label.config(text="Status: Waiting for next command...")

    # Update status when there's an error
    def update_status_error(self, error_message):
        self.status_label.config(text=f"Error: {error_message}")
        messagebox.showerror("Error", f"Failed to execute command: {error_message}")

# Main program execution
if __name__ == "__main__":
    root = tk.Tk()
    app = ControlProgram(root)
    root.mainloop()
