import customtkinter as ctk
from datetime import datetime
import os
from .functions import (
    generate_class_report, Students_data, get_student_average_grade,
    get_absence_count, get_justified_absence_count, init_managers,
    notes_manager, absence_manager
)

class ReportGenerator(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)

        init_managers()

        ctk.CTkLabel(
            self,
            text="Class Report Generator",
            font=("Montserrat", 48, "bold"),
            text_color="#3b8ed0"
        ).pack(pady=26, padx=16)

        button_frame = ctk.CTkFrame(self, corner_radius=26)
        button_frame.pack(padx=10, pady=10, fill="x")

        ctk.CTkButton(
            button_frame,
            text="Generate Global Report",
            font=("Gill Sans Nova", 16, "bold"),
            height=45,
            cursor="hand2",
            corner_radius=16,
            command=self.generate_global_report,
            fg_color="#3b8ed0"
        ).pack(side="left", padx=10, pady=10, fill="x", expand=True)

        ctk.CTkButton(
            button_frame,
            text="Export to TXT",
            font=("Gill Sans Nova", 16, "bold"),
            height=45,
            cursor="hand2",
            corner_radius=16,
            command=self.export_report
        ).pack(side="left", padx=10, pady=10)

        self.message = ctk.CTkLabel(
            self,
            text="",
            font=("Gill Sans Nova", 12),
            text_color="green"
        )
        self.message.pack(padx=10, pady=5)

        self.report_frame = ctk.CTkScrollableFrame(self, corner_radius=16)
        self.report_frame.pack(padx=10, pady=10, fill="both", expand=True)

    def generate_global_report(self):
        self.message.configure(text="", text_color="green")

        for widget in self.report_frame.winfo_children():
            widget.destroy()

        try:
            report = generate_class_report()

            title = ctk.CTkLabel(
                self.report_frame,
                text="Class Report",
                font=("Montserrat", 28, "bold"),
                text_color="#3b8ed0"
            )
            title.pack(pady=15, padx=20)

            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            time_label = ctk.CTkLabel(
                self.report_frame,
                text=f"Generated on: {timestamp}",
                font=("Gill Sans Nova", 11),
                text_color="gray"
            )
            time_label.pack(pady=5)

            summary_frame = ctk.CTkFrame(
                self.report_frame,
                corner_radius=16,
                fg_color="#e8f0ff"
            )
            summary_frame.pack(padx=20, pady=15, fill="x")

            ctk.CTkLabel(
                summary_frame,
                text="Class Summary",
                font=("Montserrat", 18, "bold"),
                text_color="#3b8ed0"
            ).pack(padx=15, pady=(10, 5))

            total = report['total_students']
            males = report['males']
            females = report['females']

            summary_text = f"""
Total Students: {total}
  • Male Students: {males}
  • Female Students: {females}
            """

            ctk.CTkLabel(
                summary_frame,
                text=summary_text.strip(),
                font=("Gill Sans Nova", 12),
                justify="left",
                text_color="#000000"
            ).pack(anchor="w", padx=20, pady=10)

            absence_frame = ctk.CTkFrame(
                self.report_frame,
                corner_radius=16,
                fg_color="#fff8e8"
            )
            absence_frame.pack(padx=20, pady=15, fill="x")

            ctk.CTkLabel(
                absence_frame,
                text="Absence Summary",
                font=("Montserrat", 18, "bold"),
                text_color="#d4a73f"
            ).pack(padx=15, pady=(10, 5))

            absence_summary = report['absence_summary']

            if absence_summary:
                header_frame = ctk.CTkFrame(absence_frame, fg_color="transparent")
                header_frame.pack(padx=20, pady=10, fill="x")

                ctk.CTkLabel(
                    header_frame,
                    text="Student",
                    font=("Gill Sans Nova", 11, "bold"),
                    width=200,
                    text_color="#000000"
                ).pack(side="left", padx=5)

                ctk.CTkLabel(
                    header_frame,
                    text="Total",
                    font=("Gill Sans Nova", 11, "bold"),
                    width=50,
                    text_color="#000000"
                ).pack(side="left", padx=5)

                ctk.CTkLabel(
                    header_frame,
                    text="Justified",
                    font=("Gill Sans Nova", 11, "bold"),
                    width=80,
                    text_color="#000000"
                ).pack(side="left", padx=5)

                ctk.CTkLabel(
                    header_frame,
                    text="Unjustified",
                    font=("Gill Sans Nova", 11, "bold"),
                    text_color="#000000"
                ).pack(side="left", padx=5)

                for record in absence_summary:
                    if record['total_absences'] > 0:
                        row_frame = ctk.CTkFrame(absence_frame, fg_color="transparent")
                        row_frame.pack(padx=20, pady=3, fill="x")

                        student_name = f"{record['first_name']} {record['last_name']}"
                        ctk.CTkLabel(
                            row_frame,
                            text=student_name,
                            font=("Gill Sans Nova", 10),
                            width=200,
                            text_color="#000000"
                        ).pack(side="left", padx=5)

                        ctk.CTkLabel(
                            row_frame,
                            text=str(record['total_absences']),
                            font=("Gill Sans Nova", 10),
                            width=50,
                            text_color="#000000"
                        ).pack(side="left", padx=5)

                        justified = record['justified_absences'] or 0
                        ctk.CTkLabel(
                            row_frame,
                            text=str(justified),
                            font=("Gill Sans Nova", 10),
                            text_color="green",
                            width=80
                        ).pack(side="left", padx=5)

                        unjustified = record['unjustified_absences'] or 0
                        ctk.CTkLabel(
                            row_frame,
                            text=str(unjustified),
                            font=("Gill Sans Nova", 10),
                            text_color="red"
                        ).pack(side="left", padx=5)
            else:
                ctk.CTkLabel(
                    absence_frame,
                    text="No absence records",
                    font=("Gill Sans Nova", 12),
                    text_color="#000000"
                ).pack(padx=20, pady=10)

            grades_frame = ctk.CTkFrame(
                self.report_frame,
                corner_radius=16,
                fg_color="#e8f8e8"
            )
            grades_frame.pack(padx=20, pady=15, fill="x")

            ctk.CTkLabel(
                grades_frame,
                text="Grades Summary",
                font=("Montserrat", 18, "bold"),
                text_color="#3b8ed0"
            ).pack(padx=15, pady=(10, 5))

            all_grades = []
            for stud in Students_data:
                avg = get_student_average_grade(stud.id)
                if avg > 0:
                    all_grades.append((f"{stud.first_name} {stud.last_name}", avg))

            if all_grades:
                header_frame = ctk.CTkFrame(grades_frame, fg_color="transparent")
                header_frame.pack(padx=20, pady=10, fill="x")

                ctk.CTkLabel(
                    header_frame,
                    text="Student",
                    font=("Gill Sans Nova", 11, "bold"),
                    width=250,
                    text_color="#000000"
                ).pack(side="left", padx=5)

                ctk.CTkLabel(
                    header_frame,
                    text="Average Grade",
                    font=("Gill Sans Nova", 11, "bold"),
                    text_color="#000000"
                ).pack(side="left", padx=5)

                all_grades.sort(key=lambda x: x[1], reverse=True)

                for student_name, avg in all_grades:
                    row_frame = ctk.CTkFrame(grades_frame, fg_color="transparent")
                    row_frame.pack(padx=20, pady=3, fill="x")

                    ctk.CTkLabel(
                        row_frame,
                        text=student_name,
                        font=("Gill Sans Nova", 10),
                        width=250,
                    text_color="#000000"
                    ).pack(side="left", padx=5)

                    grade_text = f"{avg:.2f}"
                    grade_color = "green" if avg >= 15 else "orange" if avg >= 12 else "red"
                    ctk.CTkLabel(
                        row_frame,
                        text=grade_text,
                        font=("Gill Sans Nova", 10, "bold"),
                        text_color=grade_color
                    ).pack(side="left", padx=5)
            else:
                ctk.CTkLabel(
                    grades_frame,
                    text="No grade records",
                    font=("Gill Sans Nova", 12)
                ).pack(padx=20, pady=10)

            self.message.configure(text="Report generated successfully!", text_color="green")
            self.current_report = report

        except Exception as e:
            self.message.configure(text=f"Error generating report: {str(e)}", text_color="red")

    
    def export_report(self):
        if not hasattr(self, 'current_report'):
            self.message.configure(text="Please generate a report first!", text_color="red")
            return
        
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"class_report_{timestamp}.txt"
            
            if not os.path.exists("reports"):
                os.makedirs("reports")
            
            filepath = os.path.join("reports", filename)
            
            with open(filepath, 'w', encoding='utf-8') as f:
                width = 80
                title = "CLASS REPORT"
                f.write("┌" + "─" * (width - 2) + "┐\n")
                f.write("│" + title.center(width - 2) + "│\n")
                f.write("└" + "─" * (width - 2) + "┘\n\n")

                f.write(f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write(f"Saved to: {filepath}\n\n")

                report = self.current_report

                f.write("  Class Summary\n")
                f.write("─" * width + "\n")
                f.write(f"  Total Students : {report.get('total_students', 0)}\n")
                f.write(f"  Male Students  : {report.get('males', 0)}\n")
                f.write(f"  Female Students: {report.get('females', 0)}\n")
                f.write("\n")

                f.write("  Absence Summary\n")
                f.write("─" * width + "\n")
                name_w = 36
                f.write(f"{ 'Student':<{name_w}} | {'Total':>5} | {'Just.':>6} | {'Unjust.':>7}\n")
                f.write("-" * width + "\n")

                for record in report.get('absence_summary', []):
                    if record.get('total_absences', 0) > 0:
                        student_name = f"{record.get('first_name','')} {record.get('last_name','')}".strip()
                        justified = record.get('justified_absences') or 0
                        unjustified = record.get('unjustified_absences') or 0
                        total = record.get('total_absences', 0)
                        f.write(f"{student_name:<{name_w}} | {total:>5} | {justified:>6} | {unjustified:>7}\n")

                f.write("\n")

                f.write("  Grades Summary\n")
                f.write("─" * width + "\n")
                f.write(f"{ 'Student':<{name_w}} | {'Average':>7}\n")
                f.write("-" * width + "\n")

                all_grades = []
                for stud in Students_data:
                    avg = get_student_average_grade(stud.id)
                    if avg > 0:
                        all_grades.append((f"{stud.first_name} {stud.last_name}", avg))

                all_grades.sort(key=lambda x: x[1], reverse=True)

                for student_name, avg in all_grades:
                    f.write(f"{student_name:<{name_w}} | {avg:>7.2f}\n")

                f.write("\n")
                f.write("─" * width + "\n")
            
            self.message.configure(
                text=f"Report exported successfully to {filepath}",
                text_color="green"
            )
        
        except Exception as e:
            self.message.configure(text=f"Error exporting report: {str(e)}", text_color="red")
