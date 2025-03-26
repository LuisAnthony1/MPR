from datetime import datetime, timedelta
import tkinter as tk
from tkinter import ttk, messagebox
import pywhatkit as kit
import re
import webbrowser
import urllib.parse
import os
import sys
import tempfile
import ctypes
from PIL import Image, ImageTk 
import pygame
import random
import gspread
from oauth2client.service_account import ServiceAccountCredentials

class Salkantay5DTrain:
    def __init__(self, datos):
        self.datos = datos

    def generar_confirmacion(self):
        tour = 'SALKANTAY TREK TO MACHU PICCHU 5D-4N'
        tour_dias = 4
        briefing_hora = "7:00 pm"
        primer_nombre = self.datos['nombres'][0].split()[0].capitalize()

        contenido = f"""
        <p style="color: #333;">Dear {primer_nombre},</p>
        <p style="color: #333;">Your reservation is confirmed - <span class="important">{tour}</span></p>
        
        <table>
            <tr>
                <td style="font-weight: bold; color: #00aaff;">START DATE:</td>
                <td style="color: #333;">{fecha_nombre(self.datos['fecha'][0], self.datos['fecha'][1], self.datos['fecha'][2])}</td>
            </tr>
            <tr>
                <td style="font-weight: bold; color: #00aaff;">RETURN DATE:</td>
                <td style="color: #333;">{fecha_nombre(self.datos['fecha'][0], self.datos['fecha'][1], self.datos['fecha'][2], tour_dias)}</td>
            </tr>
            <tr>
                <td style="font-weight: bold; color: #ff5555;">BRIEFING DATE:</td>
                <td style="color: #333;">{fecha_nombre(self.datos['fecha'][0], self.datos['fecha'][1], self.datos['fecha'][2], -1)}, at {briefing_hora} at Machu Picchu Reservations.</td>
            </tr>
            <tr>
                <td style="font-weight: bold; color: #00aaff;">N° PERSON:</td>
                <td style="color: #333;">{len(self.datos['nombres']):02}</td>
            </tr>
        </table>

        <ul style="margin-left: 40px; color: #333;">
            {''.join([f"<li>{i+1}. {nombre.strip().upper()}</li>" for i, nombre in enumerate(self.datos['nombres'])])}
        </ul>

        <p class="block header">TOUR INCLUSIONS:</p>
        <ul style="margin-left: 40px; color: #333;">
            <li>Transportation to the trailhead</li>
            <li>5 breakfasts</li>
            <li>4 lunches</li>
            <li>4 dinners</li>
            <li>3 comfortable nights</li>
            <li>1-night hostel in Aguas Calientes</li>
        """

        if self.datos['machu_picchu_code'] == "0":
            contenido += "<li style='color: #ff5555;'>NOT INCLUDED: Entrance for MACHU PICCHU</li>"
        else:
            contenido += f"<li>Entrance for MACHU PICCHU</li>"
            contenido += f"<li>MACHU PICCHU CODES: {self.datos['machu_picchu_code']}</li>"

        if self.datos.get('montaña', '0') != '0':
            contenido += f"<li>Entrance for {self.datos['montaña']}</li>"

        if self.datos.get('vistadome_retorno', False):
            contenido += "<li>Train from Aguas Calientes to Ollantaytambo - BY TRAIN VISTADOME</li>"
        else:
            contenido += "<li>Train from Aguas Calientes to Ollantaytambo - BY TRAIN</li>"

        contenido += f"""
            <li>Transfer from Ollantaytambo to Cusco</li>
            {"<li>{} Pair of Trekking poles</li>".format(self.datos['trekking_poles']) if self.datos['trekking_poles'] > 0 else ""}
            {"<li>{} Sleeping bags</li>".format(self.datos['sleeping_bags']) if self.datos['sleeping_bags'] > 0 else ""}
            {"<li>{} Zipline participants</li>".format(self.datos['zipline']) if self.datos.get('zipline', 0) > 0 else ""}
            <li>Guide</li>
            <li>Cooks</li>
            <li>Horses for carrying your bag</li>
        </ul>

        <p class="block header">WHAT TO PACK:</p>
        <ul style="margin-left: 40px; color: #333;">
            <li><strong>Essentials:</strong> Original passport, student card (if applicable), daypack, water storage (1.5-2L), hiking boots, headlamp.</li>
            <li><strong>Clothing (in duffel bag, max 7kg):</strong> 2-3 t-shirts, 2-3 hiking pants, 3 sets of undergarments/socks, fleece, down jacket, rain gear, sun hat, wool hat, camp shoes.</li>
            <li><strong>Gear:</strong> Waterproof gloves, rain poncho, quick-dry towel, soap, charger, plastic bags, sleeping bag (-10°C), toiletries (sunscreen, bug spray, etc.).</li>
            <li><strong>Daypack for Machu Picchu (max 25L):</strong> Water, rain gear, fleece, camera, sanitizer, extra money, earplugs.</li>
            <li><strong>Notes:</strong> Waterproof items, wear broken-in shoes, organize essentials.</li>
        </ul>

        <p class="block header">ITINERARY SUMMARY:</p>
        <p style="text-align: center;"><a href="https://www.machupicchureservations.org/tour/salkantay-trek-5-days#itinerary" target="_blank" style="text-decoration: none; color: #00aaff; font-weight: bold; padding: 8px 16px; border: 2px solid #00aaff; border-radius: 5px;">FULL ITINERARY</a></p>
        
        <ul style="margin-left: 40px; color: #333;">
            <li><strong>Day 01:</strong><br>
                &nbsp;&nbsp;• <span style="color: #55cc55;">Meals:</span> Breakfast, Lunch, Dinner<br>
                &nbsp;&nbsp;• <span style="color: #55cc55;">Accommodation:</span> Mountain Sky Hut<br>
                &nbsp;&nbsp;• <span style="color: #55cc55;">Difficulty:</span> Moderate<br>
                &nbsp;&nbsp;• <span style="color: #55cc55;">Distance:</span> 10 km (~6 miles)<br>
                &nbsp;&nbsp;• <span style="color: #55cc55;">Duration:</span> 5-6 hours<br>
                &nbsp;&nbsp;• <span style="color: #55cc55;">Elevation:</span> 4,000 m<br>
                &nbsp;&nbsp;• <span style="color: #55cc55;">Weather:</span> Cold, windy nights (-5°C in May-Aug)<br>
                &nbsp;&nbsp;• <span style="color: #55cc55;">Note:</span> Training day for acclimatization before Day 02’s challenge.
            </li>
            <li><strong>Day 02:</strong><br>
                &nbsp;&nbsp;• <span style="color: #55cc55;">Meals:</span> Breakfast, Lunch, Dinner<br>
                &nbsp;&nbsp;• <span style="color: #55cc55;">Accommodation:</span> Mountain Sky Hut<br>
                &nbsp;&nbsp;• <span style="color: #55cc55;">Difficulty:</span> Challenging<br>
                &nbsp;&nbsp;• <span style="color: #55cc55;">Max Altitude:</span> 4,700 m (Salkantay Pass)<br>
                &nbsp;&nbsp;• <span style="color: #55cc55;">Distance:</span> 22 km (~14 miles)<br>
                &nbsp;&nbsp;• <span style="color: #55cc55;">Duration:</span> 9-10 hours<br>
                &nbsp;&nbsp;• <span style="color: #55cc55;">Camping:</span> 2,900 m<br>
                &nbsp;&nbsp;• <span style="color: #55cc55;">Weather:</span> Warm and hot at lower elevations<br>
                &nbsp;&nbsp;• <span style="color: #55cc55;">Note:</span> Most difficult yet stunning day with mountain views.
            </li>
            <li><strong>Day 03:</strong><br>
                &nbsp;&nbsp;• <span style="color: #55cc55;">Meals:</span> Breakfast, Lunch, Dinner<br>
                &nbsp;&nbsp;• <span style="color: #55cc55;">Accommodation:</span> Star Domes (Crystal Domes)<br>
                &nbsp;&nbsp;• <span style="color: #55cc55;">Difficulty:</span> Easy<br>
                &nbsp;&nbsp;• <span style="color: #55cc55;">Distance:</span> 15 km (~10 miles)<br>
                &nbsp;&nbsp;• <span style="color: #55cc55;">Duration:</span> 4-5 hours<br>
                &nbsp;&nbsp;• <span style="color: #55cc55;">Camping:</span> 2,000 m<br>
                &nbsp;&nbsp;• <span style="color: #55cc55;">Weather:</span> Hot, humid day; chilly night<br>
                &nbsp;&nbsp;• <span style="color: #55cc55;">Note:</span> Relaxed Amazon exploration with coffee tour and optional hot springs.
            </li>
            <li><strong>Day 04:</strong><br>
                &nbsp;&nbsp;• <span style="color: #55cc55;">Meals:</span> Breakfast, Lunch, Dinner<br>
                &nbsp;&nbsp;• <span style="color: #55cc55;">Accommodation:</span> Hotel in Aguas Calientes<br>
                &nbsp;&nbsp;• <span style="color: #55cc55;">Difficulty:</span> Challenging<br>
                &nbsp;&nbsp;• <span style="color: #55cc55;">Max Altitude:</span> 2,700 m (Llactapata)<br>
                &nbsp;&nbsp;• <span style="color: #55cc55;">Distance:</span> 24 km (~15 miles)<br>
                &nbsp;&nbsp;• <span style="color: #55cc55;">Duration:</span> 8-9 hours<br>
                &nbsp;&nbsp;• <span style="color: #55cc55;">Town Altitude:</span> 2,000 m<br>
                &nbsp;&nbsp;• <span style="color: #55cc55;">Weather:</span> Hot<br>
                &nbsp;&nbsp;• <span style="color: #55cc55;">Note:</span> Historical Llactapata visit and descent to Aguas Calientes.
            </li>
            <li><strong>Day 05 - Explore Machu Picchu & Train Return:</strong><br>
                &nbsp;&nbsp;• <span style="color: #55cc55;">Meals:</span> Breakfast<br>
                &nbsp;&nbsp;• <span style="color: #55cc55;">Schedule:</span> Rise at 4:00 am; hike (1.5 hrs) or bus ($12, 25 min) to Machu Picchu<br>
                &nbsp;&nbsp;• <span style="color: #55cc55;">Arrival:</span> 6:00 am; show tickets/passports<br>
                &nbsp;&nbsp;• <span style="color: #55cc55;">Activities:</span> 2.5-hr guided tour + 30 min free time (max 3 hrs)<br>
                &nbsp;&nbsp;• <span style="color: #55cc55;">Optional:</span> Waynapicchu/Machu Picchu Mountain (pre-booked)<br>
                &nbsp;&nbsp;• <span style="color: #55cc55;">Return:</span> Walk (1.5 hrs) or bus ($12) to Aguas Calientes; train to Ollantaytambo (2:30/3:30 pm, 1.5 hrs); car to Cusco (2 hrs, arrive ~6:30 pm)<br>
            </li>
        </ul>
        """

        if self.datos['balance'] > 0:
            contenido += f"""
            <p class="block header">PAYMENT DETAILS:</p>
            <p style="color: #333;">Outstanding Balance: ${self.datos['balance']}. Pay online via WeTravel (2.9% fee) or in-person at our Cusco office (cash: no fee; card: 3.9% fee) before the briefing.</p>
            <p style="font-weight: bold; color: #ff55ff;">IMPORTANT: Pay up to one day before the briefing.</p>
            """

        contenido += f"""
                <div style="border-left: 4px solid #ffaa00; padding-left: 15px; margin-top: 20px;">
            <p class="block important">OFFICE LOCATION 📍:</p>
            <ul style="margin-left: 40px; color: #333; list-style-type: none; padding-left: 0;">
                <li>Portal Nuevo 270 Plaza Regocijo - Machu Picchu Reservations:</li>
            </ul>
        </div>
        
        <p style="text-align: center;"><a href="https://maps.app.goo.gl/XcfipVKjbuLeY3no9" target="_blank" style="text-decoration: none; color: #00aaff; font-weight: bold; padding: 8px 16px; border: 2px solid #00aaff; border-radius: 5px;">👉(Google Maps)👈</a></p>

        <div style="border-left: 4px solid #ffaa00; padding-left: 15px; margin-top: 20px;">
            <p class="block important">IMPORTANT:</p>
            <p style="color: #333;">Please reply to this email with passport photos and your entry date into Peru.</p>
        </div>

        <p class="block header">DETAILS YOU SHOULD KNOW:</p>
        <ul style="margin-left: 40px; color: #333;">
            <li><strong>Maximum 3 hours allowed inside Machu Picchu</strong> per park rules.</li>
            <li><strong>Bus tickets to Machu Picchu ($12)</strong> can be arranged the night before or the morning of your visit.</li>
            <li>We do not provide transportation for the briefing session. If you cannot arrive at the office on the indicated day or time, please contact 
                <a href="https://wa.me/51908851429" target="_blank"><strong>+51 908 851 429</strong></a> to receive your briefing. <strong>We recommend patience when waiting for your call to be answered.</strong> Attending the briefing session in person is strongly preferred; phone briefings are for exceptional cases like flight delays or health issues.</li>
            <li>For changes, cancellations, or to add more members to your reservation, please send a formal email to 
                <a href="https://mail.google.com/mail/?view=cm&fs=1&to=MACHUPICCHURESERVATIONS@GMAIL.COM" target="_blank"><strong>MACHUPICCHURESERVATIONS@GMAIL.COM</strong></a> with the <strong>reason for the change or cancellation attached.</strong></li>
            <li>If you wish to add <strong>trekking poles, sleeping bags, or zipline tickets</strong>, you must do so on the day of your briefing session.</li>
            <li>We do not provide <strong>private transportation</strong> for luggage or transfers within Cusco.</li>
            <li><strong>Train times may vary slightly;</strong> confirm at briefing.</li>
        </ul>

        <p style="color: #333; margin-top: 20px;">If you have any questions or need assistance, please contact <a href="https://wa.me/51908851429" 
        style="color: #ff5555; font-weight: bold;">👉MPR👈</a>. Contact us by phone call or WhatsApp message for more information or to clarify your doubts.</p>

        <div style="color: #333; font-size: 12px; margin-top: 20px;">
            <h2 style="color: #00aaff; font-size: 16px;">MACHUPICCHU RESERVATIONS</h2>
            <p><strong>Schedule:</strong> 7:00-22:00 hrs, Mon-Sat<br><strong>WhatsApp:</strong> <a href="https://api.whatsapp.com/send/?phone=51908851429" style="color: #ff5555; font-weight: bold;">👉MPR👈</a></p>
        </div>
        """

        self.mostrar_confirmacion_en_html(contenido)

    def mostrar_confirmacion_en_html(self, contenido):
        nombre_archivo = "confirmacion.html"
        with open(nombre_archivo, "w", encoding="utf-8") as file:
            file.write(f"""
            <html>
            <head>
                <title>Confirmación de Reserva</title>
                <style>
                    body {{ font-family: 'Verdana', sans-serif; margin: 20px; color: #333; }}
                    p {{ line-height: 1.6; font-size: 14px; }}
                    ul {{ list-style-type: none; padding-left: 0; }}
                    ul li::before {{ content: "•"; color: #55cc55; font-weight: bold; display: inline-block; width: 1em; margin-left: -1em; }}
                    .important {{ font-weight: bold; color: #ff5555; }}
                    .header {{ font-size: 16px; font-weight: bold; color: #00aaff; }}
                </style>
            </head>
            <body>
                {contenido}
            </body>
            </html>
            """)
        print(f"Confirmación guardada como {nombre_archivo}")

class Salkantay5DCar:
    def __init__(self, datos):
        self.datos = datos

    def generar_confirmacion(self):
        tour = 'SALKANTAY TREK TO MACHU PICCHU 5D-4N'
        tour_dias = 4
        briefing_hora = "7:00 pm"
        primer_nombre = self.datos['nombres'][0].split()[0].capitalize()

        contenido = f"""
        <p style="color: #333;">Dear {primer_nombre},</p>
        <p style="color: #333;">Your reservation is confirmed - <span class="important">{tour}</span></p>
        
        <table>
            <tr>
                <td style="font-weight: bold; color: #00aaff;">START DATE:</td>
                <td style="color: #333;">{fecha_nombre(self.datos['fecha'][0], self.datos['fecha'][1], self.datos['fecha'][2])}</td>
            </tr>
            <tr>
                <td style="font-weight: bold; color: #00aaff;">RETURN DATE:</td>
                <td style="color: #333;">{fecha_nombre(self.datos['fecha'][0], self.datos['fecha'][1], self.datos['fecha'][2], tour_dias)}</td>
            </tr>
            <tr>
                <td style="font-weight: bold; color: #ff5555;">BRIEFING DATE:</td>
                <td style="color: #333;">{fecha_nombre(self.datos['fecha'][0], self.datos['fecha'][1], self.datos['fecha'][2], -1)}, at {briefing_hora} at Machu Picchu Reservations.</td>
            </tr>
            <tr>
                <td style="font-weight: bold; color: #00aaff;">N° PERSON:</td>
                <td style="color: #333;">{len(self.datos['nombres']):02}</td>
            </tr>
        </table>

        <ul style="margin-left: 40px; color: #333;">
            {''.join([f"<li>{i+1}. {nombre.strip().upper()}</li>" for i, nombre in enumerate(self.datos['nombres'])])}
        </ul>

        <p class="block header">TOUR INCLUSIONS:</p>
        <ul style="margin-left: 40px; color: #333;">
            <li>Transportation to the trailhead</li>
            <li>5 breakfasts</li>
            <li>4 lunches</li>
            <li>4 dinners</li>
            <li>3 comfortable nights</li>
            <li>1-night hostel in Aguas Calientes</li>
        """

        if self.datos['machu_picchu_code'] == "0":
            contenido += "<li style='color: #ff5555;'>NOT INCLUDED: Entrance for MACHU PICCHU</li>"
        else:
            contenido += f"<li>Entrance for MACHU PICCHU</li>"
            contenido += f"<li>MACHU PICCHU CODES: {self.datos['machu_picchu_code']}</li>"

        contenido += f"""
            <li>Transportation from Hidroeléctrica to Cusco - BY CAR</li>
            {"<li>{} Pair of Trekking poles</li>".format(self.datos['trekking_poles']) if self.datos['trekking_poles'] > 0 else ""}
            {"<li>{} Sleeping bags</li>".format(self.datos['sleeping_bags']) if self.datos['sleeping_bags'] > 0 else ""}
            {"<li>{} Zipline participants</li>".format(self.datos['zipline']) if self.datos.get('zipline', 0) > 0 else ""}
            <li>Guide</li>
            <li>Cooks</li>
            <li>Horses for carrying your bag</li>
        </ul>

        <p class="block header">WHAT TO PACK:</p>
        <ul style="margin-left: 40px; color: #333;">
            <li><strong>Essentials:</strong> Original passport, student card (if applicable), daypack, water storage (1.5-2L), hiking boots, headlamp.</li>
            <li><strong>Clothing (in duffel bag, max 7kg):</strong> 2-3 t-shirts, 2-3 hiking pants, 3 sets of undergarments/socks, fleece, down jacket, rain gear, sun hat, wool hat, camp shoes.</li>
            <li><strong>Gear:</strong> Waterproof gloves, rain poncho, quick-dry towel, soap, charger, plastic bags, sleeping bag (-10°C), toiletries (sunscreen, bug spray, etc.).</li>
            <li><strong>Daypack for Machu Picchu (max 25L):</strong> Water, rain gear, fleece, camera, sanitizer, extra money, earplugs.</li>
            <li><strong>Notes:</strong> Waterproof items, wear broken-in shoes, organize essentials.</li>
        </ul>

        <p class="block header">ITINERARY SUMMARY:</p>
        <p style="text-align: center;"><a href="https://www.machupicchureservations.org/tour/salkantay-trek-5-days#itinerary" target="_blank" style="text-decoration: none; color: #00aaff; font-weight: bold; padding: 8px 16px; border: 2px solid #00aaff; border-radius: 5px;">FULL ITINERARY</a></p>
        
        <ul style="margin-left: 40px; color: #333;">
            <li><strong>Day 01:</strong><br>
                &nbsp;&nbsp;• <span style="color: #55cc55;">Meals:</span> Breakfast, Lunch, Dinner<br>
                &nbsp;&nbsp;• <span style="color: #55cc55;">Accommodation:</span> Mountain Sky Hut<br>
                &nbsp;&nbsp;• <span style="color: #55cc55;">Difficulty:</span> Moderate<br>
                &nbsp;&nbsp;• <span style="color: #55cc55;">Distance:</span> 10 km (~6 miles)<br>
                &nbsp;&nbsp;• <span style="color: #55cc55;">Duration:</span> 5-6 hours<br>
                &nbsp;&nbsp;• <span style="color: #55cc55;">Elevation:</span> 4,000 m<br>
                &nbsp;&nbsp;• <span style="color: #55cc55;">Weather:</span> Cold, windy nights (-5°C in May-Aug)<br>
                &nbsp;&nbsp;• <span style="color: #55cc55;">Note:</span> Training day for acclimatization before Day 02’s challenge.
            </li>
            <li><strong>Day 02:</strong><br>
                &nbsp;&nbsp;• <span style="color: #55cc55;">Meals:</span> Breakfast, Lunch, Dinner<br>
                &nbsp;&nbsp;• <span style="color: #55cc55;">Accommodation:</span> Mountain Sky Hut<br>
                &nbsp;&nbsp;• <span style="color: #55cc55;">Difficulty:</span> Challenging<br>
                &nbsp;&nbsp;• <span style="color: #55cc55;">Max Altitude:</span> 4,700 m (Salkantay Pass)<br>
                &nbsp;&nbsp;• <span style="color: #55cc55;">Distance:</span> 22 km (~14 miles)<br>
                &nbsp;&nbsp;• <span style="color: #55cc55;">Duration:</span> 9-10 hours<br>
                &nbsp;&nbsp;• <span style="color: #55cc55;">Camping:</span> 2,900 m<br>
                &nbsp;&nbsp;• <span style="color: #55cc55;">Weather:</span> Warm and hot at lower elevations<br>
                &nbsp;&nbsp;• <span style="color: #55cc55;">Note:</span> Most difficult yet stunning day with mountain views.
            </li>
            <li><strong>Day 03:</strong><br>
                &nbsp;&nbsp;• <span style="color: #55cc55;">Meals:</span> Breakfast, Lunch, Dinner<br>
                &nbsp;&nbsp;• <span style="color: #55cc55;">Accommodation:</span> Star Domes (Crystal Domes)<br>
                &nbsp;&nbsp;• <span style="color: #55cc55;">Difficulty:</span> Easy<br>
                &nbsp;&nbsp;• <span style="color: #55cc55;">Distance:</span> 15 km (~10 miles)<br>
                &nbsp;&nbsp;• <span style="color: #55cc55;">Duration:</span> 4-5 hours<br>
                &nbsp;&nbsp;• <span style="color: #55cc55;">Camping:</span> 2,000 m<br>
                &nbsp;&nbsp;• <span style="color: #55cc55;">Weather:</span> Hot, humid day; chilly night<br>
                &nbsp;&nbsp;• <span style="color: #55cc55;">Note:</span> Relaxed Amazon exploration with coffee tour and optional hot springs.
            </li>
            <li><strong>Day 04:</strong><br>
                &nbsp;&nbsp;• <span style="color: #55cc55;">Meals:</span> Breakfast, Lunch, Dinner<br>
                &nbsp;&nbsp;• <span style="color: #55cc55;">Accommodation:</span> Hotel in Aguas Calientes<br>
                &nbsp;&nbsp;• <span style="color: #55cc55;">Difficulty:</span> Challenging<br>
                &nbsp;&nbsp;• <span style="color: #55cc55;">Max Altitude:</span> 2,700 m (Llactapata)<br>
                &nbsp;&nbsp;• <span style="color: #55cc55;">Distance:</span> 24 km (~15 miles)<br>
                &nbsp;&nbsp;• <span style="color: #55cc55;">Duration:</span> 8-9 hours<br>
                &nbsp;&nbsp;• <span style="color: #55cc55;">Town Altitude:</span> 2,000 m<br>
                &nbsp;&nbsp;• <span style="color: #55cc55;">Weather:</span> Hot<br>
                &nbsp;&nbsp;• <span style="color: #55cc55;">Note:</span> Historical Llactapata visit and descent to Aguas Calientes.
            </li>
            <li><strong>Day 05 - Explore Machu Picchu & Car Return:</strong><br>
                &nbsp;&nbsp;• <span style="color: #55cc55;">Meals:</span> Breakfast<br>
                &nbsp;&nbsp;• <span style="color: #55cc55;">Schedule:</span> Rise at 4:00 am; hike (1.5 hrs) or bus ($12, 25 min) to Machu Picchu<br>
                &nbsp;&nbsp;• <span style="color: #55cc55;">Arrival:</span> 6:00 am; show tickets/passports<br>
                &nbsp;&nbsp;• <span style="color: #55cc55;">Activities:</span> 2.5-hr guided tour + 30 min free time (max 3 hrs)<br>
                &nbsp;&nbsp;• <span style="color: #55cc55;">Return:</span> Hike to Hidroeléctrica (3 hrs, leave by 11:30 am); car to Cusco (2:30 pm, 6 hrs, arrive ~10:00 pm at Plaza Regocijo)<br>
                &nbsp;&nbsp;• <span style="color: #55cc55;">Note:</span> No time for 2 circuits.
            </li>
        </ul>
        """

        if self.datos['balance'] > 0:
            contenido += f"""
            <p class="block header">PAYMENT DETAILS:</p>
            <p style="color: #333;">Outstanding Balance: ${self.datos['balance']}. Pay online via WeTravel (2.9% fee) or in-person at our Cusco office (cash: no fee; card: 3.9% fee) before the briefing.</p>
            <p style="font-weight: bold; color: #ff55ff;">IMPORTANT: Pay up to one day before the briefing.</p>
            """

        contenido += f"""
                <div style="border-left: 4px solid #ffaa00; padding-left: 15px; margin-top: 20px;">
            <p class="block important">OFFICE LOCATION 📍:</p>
            <ul style="margin-left: 40px; color: #333; list-style-type: none; padding-left: 0;">
                <li>Portal Nuevo 270 Plaza Regocijo - Machu Picchu Reservations:</li>
            </ul>
        </div>
        
        <p style="text-align: center;"><a href="https://maps.app.goo.gl/XcfipVKjbuLeY3no9" target="_blank" style="text-decoration: none; color: #00aaff; font-weight: bold; padding: 8px 16px; border: 2px solid #00aaff; border-radius: 5px;">👉(Google Maps)👈</a></p>

        <div style="border-left: 4px solid #ffaa00; padding-left: 15px; margin-top: 20px;">
            <p class="block important">IMPORTANT:</p>
            <p style="color: #333;">Please reply to this email with passport photos and your entry date into Peru.</p>
        </div>

        <p class="block header">DETAILS YOU SHOULD KNOW:</p>
        <ul style="margin-left: 40px; color: #333;">
            <li><strong>Maximum 3 hours allowed inside Machu Picchu</strong> per park rules.</li>
            <li><strong>Bus tickets to Machu Picchu ($12)</strong> can be arranged the night before or the morning of your visit.</li>
            <li><strong>Depart Machu Picchu by 11:30 AM</strong> to catch the car to Cusco at <strong>Hidroelectrica at 2:30 PM.</strong></li>
            <li>We do not provide transportation for the briefing session. If you cannot arrive at the office on the indicated day or time, please contact 
                <a href="https://wa.me/51908851429" target="_blank"><strong>+51 908 851 429</strong></a> to receive your briefing. <strong>We recommend patience when waiting for your call to be answered.</strong> Attending the briefing session in person is strongly preferred; phone briefings are for exceptional cases like flight delays or health issues.</li>
            <li>For <strong>changes, cancellations, or to add more members</strong> to your reservation, please send a formal email to 
                <a href="https://mail.google.com/mail/?view=cm&fs=1&to=MACHUPICCHURESERVATIONS@GMAIL.COM" target="_blank"><strong>MACHUPICCHURESERVATIONS@GMAIL.COM</strong></a> with the <strong>reason for the change or cancellation attached.</strong></li>
            <li>If you wish to add <strong>trekking poles, sleeping bags, or zipline tickets</strong>, you must do so on the day of your briefing session.</li>
            <li>We do not provide <strong>private transportation</strong> for luggage or transfers within Cusco.</li>
        </ul>

        <p style="color: #333; margin-top: 20px;">If you have any questions or need assistance, please contact <a href="https://wa.me/51908851429" 
        style="color: #ff5555; font-weight: bold;">👉MPR👈</a>. Contact us by phone call or WhatsApp message for more information or to clarify your doubts.</p>

        <div style="color: #333; font-size: 12px; margin-top: 20px;">
            <h2 style="color: #00aaff; font-size: 16px;">MACHUPICCHU RESERVATIONS</h2>
            <p><strong>Schedule:</strong> 7:00-22:00 hrs, Mon-Sat<br><strong>WhatsApp:</strong> <a href="https://api.whatsapp.com/send/?phone=51908851429" style="color: #ff5555; font-weight: bold;">👉MPR👈</a></p>
        </div>
        """

        self.mostrar_confirmacion_en_html(contenido)

    def mostrar_confirmacion_en_html(self, contenido, nombre_archivo="confirmacion.html"):
        with open(nombre_archivo, "w", encoding="utf-8") as file:
            file.write(f"""
            <html>
            <head>
                <title>Confirmación de Reserva</title>
                <style>
                    body {{ font-family: 'Verdana', sans-serif; margin: 20px; color: #333; }}
                    p {{ line-height: 1.6; font-size: 14px; }}
                    ul {{ list-style-type: none; padding-left: 0; }}
                    ul li::before {{ content: "•"; color: #55cc55; font-weight: bold; display: inline-block; width: 1em; margin-left: -1em; }}
                    .important {{ font-weight: bold; color: #ff5555; }}
                    .header {{ font-size: 16px; font-weight: bold; color: #00aaff; }}
                </style>
            </head>
            <body>
                {contenido}
            </body>
            </html>
            """)
        print(f"Confirmación guardada como {nombre_archivo}")

class Salkantay4DTrain:
    def __init__(self, datos):
        self.datos = datos

    def generar_confirmacion(self):
        tour = 'SALKANTAY TREK TO MACHU PICCHU 4D-3N'
        tour_dias = 3
        briefing_hora = "7:00 pm"
        primer_nombre = self.datos['nombres'][0].split()[0].capitalize()

        contenido = f"""
        <p style="color: #333;">Dear {primer_nombre},</p>
        <p style="color: #333;">Your reservation is confirmed - <span style="color: #FF69B4; font-weight: bold;">{tour}</span></p>
        
        <table>
            <tr>
                <td style="font-weight: bold; color: #FF69B4;">START DATE:</td>
                <td style="color: #333;">{fecha_nombre(self.datos['fecha'][0], self.datos['fecha'][1], self.datos['fecha'][2])}</td>
            </tr>
            <tr>
                <td style="font-weight: bold; color: #FF69B4;">RETURN DATE:</td>
                <td style="color: #333;">{fecha_nombre(self.datos['fecha'][0], self.datos['fecha'][1], self.datos['fecha'][2], tour_dias)}</td>
            </tr>
            <tr>
                <td style="font-weight: bold; color: #FF8C00;">BRIEFING DATE:</td>
                <td style="color: #333;">{fecha_nombre(self.datos['fecha'][0], self.datos['fecha'][1], self.datos['fecha'][2], -1)}, at {briefing_hora} at Machu Picchu Reservations.</td>
            </tr>
            <tr>
                <td style="font-weight: bold; color: #FF69B4;">N° PERSON:</td>
                <td style="color: #333;">{len(self.datos['nombres']):02}</td>
            </tr>
        </table>

        <ul style="margin-left: 40px; color: #333;">
            {''.join([f"<li>{i+1}. {nombre.strip().upper()}</li>" for i, nombre in enumerate(self.datos['nombres'])])}
        </ul>

        <p class="block header">TOUR INCLUSIONS:</p>
        <ul style="margin-left: 40px; color: #333;">
            <li>Transportation to the trailhead</li>
            <li>4 breakfasts</li>
            <li>3 lunches</li>
            <li>3 dinners</li>
            <li>2 comfortable nights</li>
            <li>1-night hostel in Aguas Calientes</li>
        """

        if self.datos['machu_picchu_code'] == "0":
            contenido += "<li style='color: #FF8C00;'>NOT INCLUDED: Entrance for MACHU PICCHU</li>"
        else:
            contenido += f"<li>Entrance for MACHU PICCHU</li>"
            contenido += f"<li>MACHU PICCHU CODES: {self.datos['machu_picchu_code']}</li>"

        if self.datos.get('montaña', '0') != '0':
            contenido += f"<li>Entrance for {self.datos['montaña']}</li>"

        if self.datos.get('vistadome_retorno', False):
            contenido += "<li>Train from Aguas Calientes to Ollantaytambo - BY TRAIN VISTADOME</li>"
        else:
            contenido += "<li>Train from Aguas Calientes to Ollantaytambo - BY TRAIN</li>"

        contenido += f"""
            <li>Transfer from Ollantaytambo to Cusco</li>
            {f"<li>{self.datos['sleeping_bags']} Sleeping bags</li>" if self.datos.get('sleeping_bags', 0) > 0 else ""}
            {f"<li>{self.datos['trekking_poles']} Pair of Trekking poles</li>" if self.datos.get('trekking_poles', 0) > 0 else ""}
            {f"<li>{self.datos['zipline']} Zipline participants</li>" if self.datos.get('zipline', 0) > 0 else ""}
            <li>Guide</li>
            <li>Cooks</li>
        </ul>

        <p class="block header">WHAT TO PACK:</p>
        <ul style="margin-left: 40px; color: #333;">
            <li><strong>Essentials:</strong> Original passport, student card (if applicable), daypack, water storage (1.5-2L), hiking boots, headlamp.</li>
            <li><strong>Clothing (in duffel bag, max 7kg):</strong> 2-3 t-shirts, 2-3 hiking pants, 3 sets of undergarments/socks, fleece, down jacket, rain gear, sun hat, wool hat, camp shoes.</li>
            <li><strong>Gear:</strong> Waterproof gloves, rain poncho, quick-dry towel, soap, charger, plastic bags, sleeping bag (-10°C), toiletries (sunscreen, bug spray, etc.).</li>
            <li><strong>Daypack for Machu Picchu (max 25L):</strong> Water, rain gear, fleece, camera, sanitizer, extra money, earplugs.</li>
            <li><strong>Notes:</strong> Waterproof items, wear broken-in shoes, organize essentials.</li>
        </ul>

        <p class="block header">ITINERARY SUMMARY:</p>
        <p style="text-align: center;"><a href="https://www.machupicchureservations.org/tour/salkantay-trek-4-days#itinerary" target="_blank" style="text-decoration: none; color: #FF69B4; font-weight: bold; padding: 8px 16px; border: 2px solid #FF69B4; border-radius: 5px;">FULL ITINERARY</a></p>
        
        <ul style="margin-left: 40px; color: #333;">
            <li><strong>Day 01:</strong><br>
                  • <span style="color: #32CD32;">Meals:</span> Breakfast, Lunch, Dinner<br>
                  • <span style="color: #32CD32;">Accommodation:</span> Mountain Sky Hut<br>
                  • <span style="color: #32CD32;">Difficulty:</span> Moderate<br>
                  • <span style="color: #32CD32;">Distance:</span> 10 km (~6 miles)<br>
                  • <span style="color: #32CD32;">Duration:</span> 5-6 hours<br>
                  • <span style="color: #32CD32;">Elevation:</span> 4,000 m<br>
                  • <span style="color: #32CD32;">Weather:</span> Cold, windy nights (-5°C in May-Aug)<br>
                  • <span style="color: #32CD32;">Note:</span> Training day for acclimatization before Day 02’s challenge.
            </li>
            <li><strong>Day 02:</strong><br>
                  • <span style="color: #32CD32;">Meals:</span> Breakfast, Lunch, Dinner<br>
                  • <span style="color: #32CD32;">Accommodation:</span> Mountain Sky Hut<br>
                  • <span style="color: #32CD32;">Difficulty:</span> Challenging<br>
                  • <span style="color: #32CD32;">Max Altitude:</span> 4,700 m (Salkantay Pass)<br>
                  • <span style="color: #32CD32;">Distance:</span> 22 km (~14 miles)<br>
                  • <span style="color: #32CD32;">Duration:</span> 9-10 hours<br>
                  • <span style="color: #32CD32;">Camping:</span> 2,900 m<br>
                  • <span style="color: #32CD32;">Weather:</span> Warm and hot at lower elevations<br>
                  • <span style="color: #32CD32;">Note:</span> Most difficult yet stunning day with mountain views.
            </li>
            <li><strong>Day 03:</strong><br>
                  • <span style="color: #32CD32;">Meals:</span> Breakfast, Lunch, Dinner<br>
                  • <span style="color: #32CD32;">Accommodation:</span> Hotel in Aguas Calientes<br>
                  • <span style="color: #32CD32;">Difficulty:</span> Extended Day Hike<br>
                  • <span style="color: #32CD32;">Distance:</span> ~25 km (~15 miles)<br>
                  • <span style="color: #32CD32;">Duration:</span> 9-10 hours<br>
                  • <span style="color: #32CD32;">Town Altitude:</span> 2,000 m<br>
                  • <span style="color: #32CD32;">Weather:</span> Warm, hot, tropical<br>
                  • <span style="color: #32CD32;">Note:</span> 5-hr hike, lunch, 1.5-hr car ride, 3-hr walk to Aguas Calientes.
            </li>
            <li><strong>Day 04 - Explore Machu Picchu & Train Return:</strong><br>
                  • <span style="color: #32CD32;">Meals:</span> Breakfast<br>
                  • <span style="color: #32CD32;">Schedule:</span> Rise at 4:00 am; hike (1.5 hrs) or bus ($12, 25 min) to Machu Picchu<br>
                  • <span style="color: #32CD32;">Arrival:</span> 6:00 am; show tickets/passports<br>
                  • <span style="color: #32CD32;">Activities:</span> 2.5-hr guided tour + 30 min free time (max 3 hrs)<br>
                  • <span style="color: #32CD32;">Optional:</span> Waynapicchu/Machu Picchu Mountain (pre-booked)<br>
                  • <span style="color: #32CD32;">Return:</span> Walk (1.5 hrs) or bus ($12) to Aguas Calientes; train to Ollantaytambo (2:30/3:30 pm, 1.5 hrs); car to Cusco (2 hrs, arrive ~6:30 pm)<br>
            </li>
        </ul>
        """

        if self.datos['balance'] > 0:
            contenido += f"""
            <p class="block header">PAYMENT DETAILS:</p>
            <p style="color: #333;">Outstanding Balance: ${self.datos['balance']}. Pay online via WeTravel (2.9% fee) or in-person at our Cusco office (cash: no fee; card: 3.9% fee) before the briefing.</p>
            <p style="font-weight: bold; color: #FF1493;">IMPORTANT: Pay up to one day before the briefing.</p>
            """

        contenido += f"""
                <div style="border-left: 4px solid #ffaa00; padding-left: 15px; margin-top: 20px;">
            <p class="block important">OFFICE LOCATION 📍:</p>
            <ul style="margin-left: 40px; color: #333; list-style-type: none; padding-left: 0;">
                <li>Portal Nuevo 270 Plaza Regocijo - Machu Picchu Reservations:</li>
            </ul>
        </div>
        
        <p style="text-align: center;"><a href="https://maps.app.goo.gl/XcfipVKjbuLeY3no9" target="_blank" style="text-decoration: none; color: #00aaff; font-weight: bold; padding: 8px 16px; border: 2px solid #00aaff; border-radius: 5px;">👉(Google Maps)👈</a></p>

        <div style="border-left: 4px solid #ffaa00; padding-left: 15px; margin-top: 20px;">
            <p class="block important">IMPORTANT:</p>
            <p style="color: #333;">Please reply to this email with passport photos and your entry date into Peru.</p>
        </div>

        <p class="block header">DETAILS YOU SHOULD KNOW:</p>
        <ul style="margin-left: 40px; color: #333;">
            <li><strong>Maximum 3 hours allowed inside Machu Picchu</strong> per park rules.</li>
            <li><strong>Bus tickets to Machu Picchu ($12)</strong> can be arranged the night before or the morning of your visit.</li>
            <li>We do not provide transportation for the briefing session. If you cannot arrive at the office on the indicated day or time, please contact 
                <a href="https://wa.me/51908851429" target="_blank"><strong>+51 908 851 429</strong></a> to receive your briefing. <strong>We recommend patience when waiting for your call to be answered.</strong> Attending the briefing session in person is strongly preferred; phone briefings are for exceptional cases like flight delays or health issues.</li>
            <li>For changes, cancellations, or to add more members to your reservation, please send a formal email to 
                <a href="https://mail.google.com/mail/?view=cm&fs=1&to=MACHUPICCHURESERVATIONS@GMAIL.COM" target="_blank"><strong>MACHUPICCHURESERVATIONS@GMAIL.COM</strong></a> with the <strong>reason for the change or cancellation attached.</strong></li>
            <li>If you wish to add <strong>trekking poles, sleeping bags, or zipline tickets</strong>, you must do so on the day of your briefing session.</li>
            <li>We do not provide <strong>private transportation</strong> for luggage or transfers within Cusco.</li>
            <li><strong>Train times may vary slightly;</strong> confirm at briefing.</li>
        </ul>

        <p style="color: #333; margin-top: 20px;">If you have any questions or need assistance, please contact <a href="https://wa.me/51908851429" 
        style="color: #ff5555; font-weight: bold;">👉MPR👈</a>. Contact us by phone call or WhatsApp message for more information or to clarify your doubts.</p>

        <div style="color: #333; font-size: 12px; margin-top: 20px;">
            <h2 style="color: #00aaff; font-size: 16px;">MACHUPICCHU RESERVATIONS</h2>
            <p><strong>Schedule:</strong> 7:00-22:00 hrs, Mon-Sat<br><strong>WhatsApp:</strong> <a href="https://api.whatsapp.com/send/?phone=51908851429" style="color: #ff5555; font-weight: bold;">👉MPR👈</a></p>
        </div>
        """

        self.mostrar_confirmacion_en_html(contenido)

    def mostrar_confirmacion_en_html(self, contenido):
        nombre_archivo = "confirmacion.html"
        with open(nombre_archivo, "w", encoding="utf-8") as file:
            file.write(f"""
            <html>
            <head>
                <title>Confirmación de Reserva</title>
                <style>
                    body {{ font-family: 'Verdana', sans-serif; margin: 20px; color: #333; }}
                    p {{ line-height: 1.6; font-size: 14px; }}
                    ul {{ list-style-type: none; padding-left: 0; }}
                    ul li::before {{ content: "•"; color: #32CD32; font-weight: bold; display: inline-block; width: 1em; margin-left: -1em; }}
                    .important {{ font-weight: bold; color: #FF8C00; }}
                    .header {{ font-size: 16px; font-weight: bold; color: #FF69B4; }}
                </style>
            </head>
            <body>
                {contenido}
            </body>
            </html>
            """)
        print(f"Confirmación guardada como {nombre_archivo}")

class Salkantay4DCar:
    def __init__(self, datos):
        self.datos = datos

    def generar_confirmacion(self):
        tour = 'SALKANTAY TREK TO MACHU PICCHU 4D-3N'
        tour_dias = 3
        briefing_hora = "7:00 pm"
        primer_nombre = self.datos['nombres'][0].split()[0].capitalize()

        contenido = f"""
        <p style="color: #333;">Dear {primer_nombre},</p>
        <p style="color: #333;">Your reservation is confirmed - <span style="color: #FF69B4; font-weight: bold;">{tour}</span></p>
        
        <table>
            <tr>
                <td style="font-weight: bold; color: #FF69B4;">START DATE:</td>
                <td style="color: #333;">{fecha_nombre(self.datos['fecha'][0], self.datos['fecha'][1], self.datos['fecha'][2])}</td>
            </tr>
            <tr>
                <td style="font-weight: bold; color: #FF69B4;">RETURN DATE:</td>
                <td style="color: #333;">{fecha_nombre(self.datos['fecha'][0], self.datos['fecha'][1], self.datos['fecha'][2], tour_dias)}</td>
            </tr>
            <tr>
                <td style="font-weight: bold; color: #FF8C00;">BRIEFING DATE:</td>
                <td style="color: #333;">{fecha_nombre(self.datos['fecha'][0], self.datos['fecha'][1], self.datos['fecha'][2], -1)}, at {briefing_hora} at Machu Picchu Reservations.</td>
            </tr>
            <tr>
                <td style="font-weight: bold; color: #FF69B4;">N° PERSON:</td>
                <td style="color: #333;">{len(self.datos['nombres']):02}</td>
            </tr>
        </table>

        <ul style="margin-left: 40px; color: #333;">
            {''.join([f"<li>{i+1}. {nombre.strip().upper()}</li>" for i, nombre in enumerate(self.datos['nombres'])])}
        </ul>

        <p class="block header">TOUR INCLUSIONS:</p>
        <ul style="margin-left: 40px; color: #333;">
            <li>Transportation to the trailhead</li>
            <li>4 breakfasts</li>
            <li>3 lunches</li>
            <li>3 dinners</li>
            <li>2 comfortable nights</li>
            <li>1-night hostel in Aguas Calientes</li>
        """

        if self.datos['machu_picchu_code'] == "0":
            contenido += "<li style='color: #FF8C00;'>NOT INCLUDED: Entrance for MACHU PICCHU</li>"
        else:
            contenido += f"<li>Entrance for MACHU PICCHU</li>"
            contenido += f"<li>MACHU PICCHU CODES: {self.datos['machu_picchu_code']}</li>"

        contenido += f"""
            <li>Transportation from Hidroeléctrica to Cusco - BY CAR</li>
            {f"<li>{self.datos['sleeping_bags']} Sleeping bags</li>" if self.datos.get('sleeping_bags', 0) > 0 else ""}
            {f"<li>{self.datos['trekking_poles']} Pair of Trekking poles</li>" if self.datos.get('trekking_poles', 0) > 0 else ""}
            {f"<li>{self.datos['zipline']} Zipline participants</li>" if self.datos.get('zipline', 0) > 0 else ""}
            <li>Guide</li>
            <li>Cooks</li>
            <li>Horses for carrying your bag</li>
        </ul>

        <p class="block header">WHAT TO PACK:</p>
        <ul style="margin-left: 40px; color: #333;">
            <li><strong>Essentials:</strong> Original passport, student card (if applicable), daypack, water storage (1.5-2L), hiking boots, headlamp.</li>
            <li><strong>Clothing (in duffel bag, max 7kg):</strong> 2-3 t-shirts, 2-3 hiking pants, 3 sets of undergarments/socks, fleece, down jacket, rain gear, sun hat, wool hat, camp shoes.</li>
            <li><strong>Gear:</strong> Waterproof gloves, rain poncho, quick-dry towel, soap, charger, plastic bags, sleeping bag (-10°C), toiletries (sunscreen, bug spray, etc.).</li>
            <li><strong>Daypack for Machu Picchu (max 25L):</strong> Water, rain gear, fleece, camera, sanitizer, extra money, earplugs.</li>
            <li><strong>Notes:</strong> Waterproof items, wear broken-in shoes, organize essentials.</li>
        </ul>

        <p class="block header">ITINERARY SUMMARY:</p>
        <p style="text-align: center;"><a href="https://www.machupicchureservations.org/tour/salkantay-trek-4-days#itinerary" target="_blank" style="text-decoration: none; color: #FF69B4; font-weight: bold; padding: 8px 16px; border: 2px solid #FF69B4; border-radius: 5px;">FULL ITINERARY</a></p>
        
        <ul style="margin-left: 40px; color: #333;">
            <li><strong>Day 01:</strong><br>
                  • <span style="color: #32CD32;">Meals:</span> Breakfast, Lunch, Dinner<br>
                  • <span style="color: #32CD32;">Accommodation:</span> Mountain Sky Hut<br>
                  • <span style="color: #32CD32;">Difficulty:</span> Moderate<br>
                  • <span style="color: #32CD32;">Distance:</span> 10 km (~6 miles)<br>
                  • <span style="color: #32CD32;">Duration:</span> 5-6 hours<br>
                  • <span style="color: #32CD32;">Elevation:</span> 4,000 m<br>
                  • <span style="color: #32CD32;">Weather:</span> Cold, windy nights (-5°C in May-Aug)<br>
                  • <span style="color: #32CD32;">Note:</span> Training day for acclimatization before Day 02’s challenge.
            </li>
            <li><strong>Day 02:</strong><br>
                  • <span style="color: #32CD32;">Meals:</span> Breakfast, Lunch, Dinner<br>
                  • <span style="color: #32CD32;">Accommodation:</span> Mountain Sky Hut<br>
                  • <span style="color: #32CD32;">Difficulty:</span> Challenging<br>
                  • <span style="color: #32CD32;">Max Altitude:</span> 4,700 m (Salkantay Pass)<br>
                  • <span style="color: #32CD32;">Distance:</span> 22 km (~14 miles)<br>
                  • <span style="color: #32CD32;">Duration:</span> 9-10 hours<br>
                  • <span style="color: #32CD32;">Camping:</span> 2,900 m<br>
                  • <span style="color: #32CD32;">Weather:</span> Warm and hot at lower elevations<br>
                  • <span style="color: #32CD32;">Note:</span> Most difficult yet stunning day with mountain views.
            </li>
            <li><strong>Day 03:</strong><br>
                  • <span style="color: #32CD32;">Meals:</span> Breakfast, Lunch, Dinner<br>
                  • <span style="color: #32CD32;">Accommodation:</span> Hotel in Aguas Calientes<br>
                  • <span style="color: #32CD32;">Difficulty:</span> Extended Day Hike<br>
                  • <span style="color: #32CD32;">Distance:</span> ~25 km (~15 miles)<br>
                  • <span style="color: #32CD32;">Duration:</span> 9-10 hours<br>
                  • <span style="color: #32CD32;">Town Altitude:</span> 2,000 m<br>
                  • <span style="color: #32CD32;">Weather:</span> Warm, hot, tropical<br>
                  • <span style="color: #32CD32;">Note:</span> 5-hr hike, lunch, 1.5-hr car ride, 3-hr walk to Aguas Calientes.
            </li>
            <li><strong>Day 04 - Explore Machu Picchu & Car Return:</strong><br>
                  • <span style="color: #32CD32;">Meals:</span> Breakfast<br>
                  • <span style="color: #32CD32;">Schedule:</span> Rise at 4:00 am; hike (1.5 hrs) or bus ($12, 25 min) to Machu Picchu<br>
                  • <span style="color: #32CD32;">Arrival:</span> 6:00 am; show tickets/passports<br>
                  • <span style="color: #32CD32;">Activities:</span> 2.5-hr guided tour + 30 min free time (max 3 hrs)<br>
                  • <span style="color: #32CD32;">Return:</span> Hike to Hidroeléctrica (3 hrs, leave by 11:30 am); car to Cusco (2:30 pm, 6 hrs, arrive ~10:00 pm at Plaza Regocijo)<br>
            </li>
        </ul>
        """

        if self.datos['balance'] > 0:
            contenido += f"""
            <p class="block header">PAYMENT DETAILS:</p>
            <p style="color: #333;">Outstanding Balance: ${self.datos['balance']}. Pay online via WeTravel (2.9% fee) or in-person at our Cusco office (cash: no fee; card: 3.9% fee) before the briefing.</p>
            <p style="font-weight: bold; color: #FF1493;">IMPORTANT: Pay up to one day before the briefing.</p>
            """

        contenido += f"""
                <div style="border-left: 4px solid #ffaa00; padding-left: 15px; margin-top: 20px;">
            <p class="block important">OFFICE LOCATION 📍:</p>
            <ul style="margin-left: 40px; color: #333; list-style-type: none; padding-left: 0;">
                <li>Portal Nuevo 270 Plaza Regocijo - Machu Picchu Reservations:</li>
            </ul>
        </div>
        
        <p style="text-align: center;"><a href="https://maps.app.goo.gl/XcfipVKjbuLeY3no9" target="_blank" style="text-decoration: none; color: #00aaff; font-weight: bold; padding: 8px 16px; border: 2px solid #00aaff; border-radius: 5px;">👉(Google Maps)👈</a></p>

        <div style="border-left: 4px solid #ffaa00; padding-left: 15px; margin-top: 20px;">
            <p class="block important">IMPORTANT:</p>
            <p style="color: #333;">Please reply to this email with passport photos and your entry date into Peru.</p>
        </div>

        <p class="block header">DETAILS YOU SHOULD KNOW:</p>
        <ul style="margin-left: 40px; color: #333;">
            <li><strong>Maximum 3 hours allowed inside Machu Picchu</strong> per park rules.</li>
            <li><strong>Bus tickets to Machu Picchu ($12)</strong> can be arranged the night before or the morning of your visit.</li>
            <li><strong>Depart Machu Picchu by 11:30 AM</strong> to catch the car to Cusco at <strong>Hidroelectrica at 2:30 PM.</strong></li>
            <li>We do not provide transportation for the briefing session. If you cannot arrive at the office on the indicated day or time, please contact 
                <a href="https://wa.me/51908851429" target="_blank"><strong>+51 908 851 429</strong></a> to receive your briefing. <strong>We recommend patience when waiting for your call to be answered.</strong> Attending the briefing session in person is strongly preferred; phone briefings are for exceptional cases like flight delays or health issues.</li>
            <li>For <strong>changes, cancellations, or to add more members</strong> to your reservation, please send a formal email to 
                <a href="https://mail.google.com/mail/?view=cm&fs=1&to=MACHUPICCHURESERVATIONS@GMAIL.COM" target="_blank"><strong>MACHUPICCHURESERVATIONS@GMAIL.COM</strong></a> with the <strong>reason for the change or cancellation attached.</strong></li>
            <li>If you wish to add <strong>trekking poles, sleeping bags, or zipline tickets</strong>, you must do so on the day of your briefing session.</li>
            <li>We do not provide <strong>private transportation</strong> for luggage or transfers within Cusco.</li>
        </ul>

        <p style="color: #333; margin-top: 20px;">If you have any questions or need assistance, please contact <a href="https://wa.me/51908851429" 
        style="color: #ff5555; font-weight: bold;">👉MPR👈</a>. Contact us by phone call or WhatsApp message for more information or to clarify your doubts.</p>

        <div style="color: #333; font-size: 12px; margin-top: 20px;">
            <h2 style="color: #00aaff; font-size: 16px;">MACHUPICCHU RESERVATIONS</h2>
            <p><strong>Schedule:</strong> 7:00-22:00 hrs, Mon-Sat<br><strong>WhatsApp:</strong> <a href="https://api.whatsapp.com/send/?phone=51908851429" style="color: #ff5555; font-weight: bold;">👉MPR👈</a></p>
        </div>
        """

        self.mostrar_confirmacion_en_html(contenido)

    def mostrar_confirmacion_en_html(self, contenido, nombre_archivo="confirmacion.html"):
        with open(nombre_archivo, "w", encoding="utf-8") as file:
            file.write(f"""
            <html>
            <head>
                <title>Confirmación de Reserva</title>
                <style>
                    body {{ font-family: 'Verdana', sans-serif; margin: 20px; color: #333; }}
                    p {{ line-height: 1.6; font-size: 14px; }}
                    ul {{ list-style-type: none; padding-left: 0; }}
                    ul li::before {{ content: "•"; color: #32CD32; font-weight: bold; display: inline-block; width: 1em; margin-left: -1em; }}
                    .important {{ font-weight: bold; color: #FF8C00; }}
                    .header {{ font-size: 16px; font-weight: bold; color: #FF69B4; }}
                </style>
            </head>
            <body>
                {contenido}
            </body>
            </html>
            """)
        print(f"Confirmación guardada como {nombre_archivo}")

class Salkantay3DTrain:
    def __init__(self, datos):
        if datos is None or not isinstance(datos, dict):
            raise ValueError("Se requiere un diccionario de datos válido")
        self.datos = datos

    def generar_confirmacion(self):
        if 'nombres' not in self.datos or not self.datos['nombres']:
            raise ValueError("El diccionario de datos no contiene la clave 'nombres' o está vacío.")

        tour = 'SALKANTAY TREK TO MACHU PICCHU 3D-2N'
        tour_dias = 2
        briefing_hora = "7:00 pm"
        primer_nombre = self.datos['nombres'][0].split()[0].capitalize()

        contenido = f"""
        <p style="color: #333;">Dear {primer_nombre},</p>
        <p style="color: #333;">Your reservation is confirmed - <span style="color: #20B2AA; font-weight: bold;">{tour}</span></p>
        
        <table>
            <tr>
                <td style="font-weight: bold; color: #20B2AA;">START DATE:</td>
                <td style="color: #333;">{fecha_nombre(self.datos['fecha'][0], self.datos['fecha'][1], self.datos['fecha'][2])}</td>
            </tr>
            <tr>
                <td style="font-weight: bold; color: #20B2AA;">RETURN DATE:</td>
                <td style="color: #333;">{fecha_nombre(self.datos['fecha'][0], self.datos['fecha'][1], self.datos['fecha'][2], tour_dias)}</td>
            </tr>
            <tr>
                <td style="font-weight: bold; color: #FFA500;">BRIEFING DATE:</td>
                <td style="color: #333;">{fecha_nombre(self.datos['fecha'][0], self.datos['fecha'][1], self.datos['fecha'][2], -1)}, at {briefing_hora} at Machu Picchu Reservations.</td>
            </tr>
            <tr>
                <td style="font-weight: bold; color: #20B2AA;">N° PERSON:</td>
                <td style="color: #333;">{len(self.datos['nombres']):02}</td>
            </tr>
        </table>

        <ul style="margin-left: 40px; color: #333;">
            {''.join([f"<li>{i+1}. {nombre.strip().upper()}</li>" for i, nombre in enumerate(self.datos['nombres'])])}
        </ul>

        <p class="block header">TOUR INCLUSIONS:</p>
        <ul style="margin-left: 40px; color: #333;">
            <li>Transportation to the trailhead</li>
            <li>3 breakfasts</li>
            <li>2 lunches</li>
            <li>2 dinners</li>
            <li>1 comfortable night</li>
            <li>1-night hostel in Aguas Calientes</li>
        """

        if self.datos['machu_picchu_code'] == "0":
            contenido += "<li style='color: #FFA500;'>NOT INCLUDED: Entrance for MACHU PICCHU</li>"
        else:
            contenido += f"<li>Entrance for MACHU PICCHU</li>"
            contenido += f"<li>MACHU PICCHU CODES: {self.datos['machu_picchu_code']}</li>"

        if self.datos.get('montaña', '0') != '0':
            contenido += f"<li>Entrance for {self.datos['montaña']}</li>"

        if self.datos.get('vistadome_retorno', False):
            contenido += "<li>Train from Aguas Calientes to Ollantaytambo - BY TRAIN VISTADOME</li>"
        else:
            contenido += "<li>Train from Aguas Calientes to Ollantaytambo - BY TRAIN</li>"

        contenido += f"""
            <li>Transfer from Ollantaytambo to Cusco</li>
            {f"<li>{self.datos['sleeping_bags']} Sleeping bags</li>" if self.datos.get('sleeping_bags', 0) > 0 else ""}
            {f"<li>{self.datos['trekking_poles']} Pair of Trekking poles</li>" if self.datos.get('trekking_poles', 0) > 0 else ""}
            <li>Guide</li>
            <li>Cooks</li>
            <li>Horses for carrying your bag</li>
        </ul>

        <p class="block header">WHAT TO PACK:</p>
        <ul style="margin-left: 40px; color: #333;">
            <li><strong>Essentials:</strong> Original passport, student card (if applicable), 20-30L daypack.</li>
            <li><strong>Clothing:</strong> Wool hat, sun hat, scarf, gloves, 2-3 long-sleeve t-shirts, 2 layers (sweater, fleece), 2 pairs long pants/leggings, hiking shoes, 2 pairs wool socks, shorts, sandals.</li>
            <li><strong>Gear:</strong> Headlamp, towel, sunscreen, insect repellent, sunglasses, toiletries, toilet paper, water bottle, rain gear (poncho/jacket/pants), optional thermal clothing.</li>
            <li><strong>Extras:</strong> Snacks (chocolate, nuts, etc.), extra cash in Soles.</li>
            <li><strong>Note:</strong> We provide a 7kg duffle bag carried by horses; you carry your daypack.</li>
        </ul>

        <p class="block header">ITINERARY SUMMARY:</p>
        <p style="text-align: center;"><a href="https://www.machupicchureservations.org/tour/salkantay-trek-3-days#itinerary" target="_blank" style="text-decoration: none; color: #20B2AA; font-weight: bold; padding: 8px 16px; border: 2px solid #20B2AA; border-radius: 5px;">FULL ITINERARY</a></p>
        
        <ul style="margin-left: 40px; color: #333;">
            <li><strong>Day 01:</strong><br>
                  • <span style="color: #ADFF2F;">Meals:</span> Breakfast, Lunch, Tea, Dinner<br>
                  • <span style="color: #ADFF2F;">Accommodation:</span> Star Domes<br>
                  • <span style="color: #ADFF2F;">Distance:</span> 22 km (~9 hrs)<br>
                  • <span style="color: #ADFF2F;">Max Altitude:</span> 4,650 m<br>
                  • <span style="color: #ADFF2F;">Campsite:</span> 2,000 m (Lucmabamba)<br>
                  • <span style="color: #ADFF2F;">Weather:</span> Warm, windy day; cold night<br>
                  • <span style="color: #ADFF2F;">Note:</span> Conquer the trek’s highest point.
            </li>
            <li><strong>Day 02:</strong><br>
                  • <span style="color: #ADFF2F;">Meals:</span> Breakfast, Lunch, Dinner<br>
                  • <span style="color: #ADFF2F;">Accommodation:</span> Hotel in Aguas Calientes<br>
                  • <span style="color: #ADFF2F;">Difficulty:</span> Challenging<br>
                  • <span style="color: #ADFF2F;">Distance:</span> 24 km (~15 miles)<br>
                  • <span style="color: #ADFF2F;">Duration:</span> 8-9 hours<br>
                  • <span style="color: #ADFF2F;">Max Altitude:</span> 2,700 m (Llactapata)<br>
                  • <span style="color: #ADFF2F;">Town Altitude:</span> 2,000 m<br>
                  • <span style="color: #ADFF2F;">Weather:</span> Hot
            </li>
            <li><strong>Day 03 - Machu Picchu & Train Return:</strong><br>
                  • <span style="color: #ADFF2F;">Meals:</span> Breakfast<br>
                  • <span style="color: #ADFF2F;">Schedule:</span> Rise at 4:00 am; hike (1.5 hrs) or bus ($12, 30 min) to Machu Picchu<br>
                  • <span style="color: #ADFF2F;">Arrival:</span> 6:00 am; show tickets/passports<br>
                  • <span style="color: #ADFF2F;">Activities:</span> 2.5-hr guided tour (Circuit 01/02 preferred); optional Huayna Picchu/Machu Picchu Mountain ($60, pre-booked)<br>
                  • <span style="color: #ADFF2F;">Return:</span> Walk (1.5 hrs) or bus ($12) to Aguas Calientes; train to Ollantaytambo (2:30/2:55 pm, 1.5 hrs); car to Cusco (2 hrs, arrive ~6:30 pm)<br>
            </li>
        </ul>
        """

        if self.datos['balance'] > 0:
            contenido += f"""
            <p class="block header">PAYMENT DETAILS:</p>
            <p style="color: #333;">Outstanding Balance: ${self.datos['balance']}. Pay online via WeTravel (2.9% fee) or in-person at our Cusco office (cash: no fee; card: 3.9% fee) before the briefing.</p>
            <p style="font-weight: bold; color: #FF4500;">IMPORTANT: Pay up to one day before the briefing.</p>
            """

        contenido += f"""
                <div style="border-left: 4px solid #ffaa00; padding-left: 15px; margin-top: 20px;">
            <p class="block important">OFFICE LOCATION 📍:</p>
            <ul style="margin-left: 40px; color: #333; list-style-type: none; padding-left: 0;">
                <li>Portal Nuevo 270 Plaza Regocijo - Machu Picchu Reservations:</li>
            </ul>
        </div>
        
        <p style="text-align: center;"><a href="https://maps.app.goo.gl/XcfipVKjbuLeY3no9" target="_blank" style="text-decoration: none; color: #00aaff; font-weight: bold; padding: 8px 16px; border: 2px solid #00aaff; border-radius: 5px;">👉(Google Maps)👈</a></p>

        <div style="border-left: 4px solid #ffaa00; padding-left: 15px; margin-top: 20px;">
            <p class="block important">IMPORTANT:</p>
            <p style="color: #333;">Please reply to this email with passport photos and your entry date into Peru.</p>
        </div>

        <p class="block header">DETAILS YOU SHOULD KNOW:</p>
        <ul style="margin-left: 40px; color: #333;">
            <li><strong>Maximum 3 hours allowed inside Machu Picchu</strong> per park rules.</li>
            <li><strong>Bus tickets to Machu Picchu ($12)</strong> can be arranged the night before or the morning of your visit.</li>
            <li>We do not provide transportation for the briefing session. If you cannot arrive at the office on the indicated day or time, please contact 
                <a href="https://wa.me/51908851429" target="_blank"><strong>+51 908 851 429</strong></a> to receive your briefing. <strong>We recommend patience when waiting for your call to be answered.</strong> Attending the briefing session in person is strongly preferred; phone briefings are for exceptional cases like flight delays or health issues.</li>
            <li>For changes, cancellations, or to add more members to your reservation, please send a formal email to 
                <a href="https://mail.google.com/mail/?view=cm&fs=1&to=MACHUPICCHURESERVATIONS@GMAIL.COM" target="_blank"><strong>MACHUPICCHURESERVATIONS@GMAIL.COM</strong></a> with the <strong>reason for the change or cancellation attached.</strong></li>
            <li>If you wish to add <strong>trekking poles or sleeping bags</strong>, you must do so on the day of your briefing session.</li>
            <li>We do not provide <strong>private transportation</strong> for luggage or transfers within Cusco.</li>
            <li><strong>Train times may vary slightly;</strong> confirm at briefing.</li>
        </ul>

        <p style="color: #333; margin-top: 20px;">If you have any questions or need assistance, please contact <a href="https://wa.me/51908851429" 
        style="color: #ff5555; font-weight: bold;">👉MPR👈</a>. Contact us by phone call or WhatsApp message for more information or to clarify your doubts.</p>

        <div style="color: #333; font-size: 12px; margin-top: 20px;">
            <h2 style="color: #00aaff; font-size: 16px;">MACHUPICCHU RESERVATIONS</h2>
            <p><strong>Schedule:</strong> 7:00-22:00 hrs, Mon-Sat<br><strong>WhatsApp:</strong> <a href="https://api.whatsapp.com/send/?phone=51908851429" style="color: #ff5555; font-weight: bold;">👉MPR👈</a></p>
        </div>
        """

        self.mostrar_confirmacion_en_html(contenido)

    def mostrar_confirmacion_en_html(self, contenido):
        nombre_archivo = "confirmacion.html"
        with open(nombre_archivo, "w", encoding="utf-8") as file:
            file.write(f"""
            <html>
            <head>
                <title>Confirmación de Reserva</title>
                <style>
                    body {{ font-family: 'Verdana', sans-serif; margin: 20px; color: #333; }}
                    p {{ line-height: 1.6; font-size: 14px; }}
                    ul {{ list-style-type: none; padding-left: 0; }}
                    ul li::before {{ content: "•"; color: #ADFF2F; font-weight: bold; display: inline-block; width: 1em; margin-left: -1em; }}
                    .important {{ font-weight: bold; color: #FFA500; }}
                    .header {{ font-size: 16px; font-weight: bold; color: #20B2AA; }}
                </style>
            </head>
            <body>
                {contenido}
            </body>
            </html>
            """)
        print(f"Confirmación guardada como {nombre_archivo}")

class Salkantay3DCar:
    def __init__(self, datos):
        self.datos = datos

    def generar_confirmacion(self):
        tour = 'SALKANTAY TREK TO MACHU PICCHU 3D-2N'
        tour_dias = 2
        briefing_hora = "7:00 pm"
        primer_nombre = self.datos['nombres'][0].split()[0].capitalize()

        contenido = f"""
        <p style="color: #333;">Dear {primer_nombre},</p>
        <p style="color: #333;">Your reservation is confirmed - <span style="color: #20B2AA; font-weight: bold;">{tour}</span></p>
        
        <table>
            <tr>
                <td style="font-weight: bold; color: #20B2AA;">START DATE:</td>
                <td style="color: #333;">{fecha_nombre(self.datos['fecha'][0], self.datos['fecha'][1], self.datos['fecha'][2])}</td>
            </tr>
            <tr>
                <td style="font-weight: bold; color: #20B2AA;">RETURN DATE:</td>
                <td style="color: #333;">{fecha_nombre(self.datos['fecha'][0], self.datos['fecha'][1], self.datos['fecha'][2], tour_dias)}</td>
            </tr>
            <tr>
                <td style="font-weight: bold; color: #FFA500;">BRIEFING DATE:</td>
                <td style="color: #333;">{fecha_nombre(self.datos['fecha'][0], self.datos['fecha'][1], self.datos['fecha'][2], -1)}, at {briefing_hora} at Machu Picchu Reservations.</td>
            </tr>
            <tr>
                <td style="font-weight: bold; color: #20B2AA;">N° PERSON:</td>
                <td style="color: #333;">{len(self.datos['nombres']):02}</td>
            </tr>
        </table>

        <ul style="margin-left: 40px; color: #333;">
            {''.join([f"<li>{i+1}. {nombre.strip().upper()}</li>" for i, nombre in enumerate(self.datos['nombres'])])}
        </ul>

        <p class="block header">TOUR INCLUSIONS:</p>
        <ul style="margin-left: 40px; color: #333;">
            <li>Transportation to the trailhead</li>
            <li>3 breakfasts</li>
            <li>2 lunches</li>
            <li>2 dinners</li>
            <li>1 comfortable night</li>
            <li>1-night hostel in Aguas Calientes</li>
        """

        if self.datos['machu_picchu_code'] == "0":
            contenido += "<li style='color: #FFA500;'>NOT INCLUDED: Entrance for MACHU PICCHU</li>"
        else:
            contenido += f"<li>Entrance for MACHU PICCHU</li>"
            contenido += f"<li>MACHU PICCHU CODES: {self.datos['machu_picchu_code']}</li>"

        contenido += f"""
            <li>Transportation from Hidroeléctrica to Cusco - BY CAR</li>
            {"<li>{self.datos['sleeping_bags']} Sleeping bags</li>" if self.datos.get('sleeping_bags', 0) > 0 else ""}
            {"<li>{self.datos['trekking_poles']} Pair of Trekking poles</li>" if self.datos.get('trekking_poles', 0) > 0 else ""}
            <li>Guide</li>
            <li>Cooks</li>
            <li>Horses for carrying your bag</li>
        </ul>

        <p class="block header">WHAT TO PACK:</p>
        <ul style="margin-left: 40px; color: #333;">
            <li><strong>Essentials:</strong> Original passport, student card (if applicable), 20-30L daypack.</li>
            <li><strong>Clothing:</strong> Wool hat, sun hat, scarf, gloves, 2-3 long-sleeve t-shirts, 2 layers (sweater, fleece), 2 pairs long pants/leggings, hiking shoes, 2 pairs wool socks, shorts, sandals.</li>
            <li><strong>Gear:</strong> Headlamp, towel, sunscreen, insect repellent, sunglasses, toiletries, toilet paper, water bottle, rain gear (poncho/jacket/pants), optional thermal clothing.</li>
            <li><strong>Extras:</strong> Snacks (chocolate, nuts, etc.), extra cash in Soles.</li>
            <li><strong>Note:</strong> We provide a 7kg duffle bag carried by horses; you carry your daypack.</li>
        </ul>

        <p class="block header">ITINERARY SUMMARY:</p>
        <p style="text-align: center;"><a href="https://www.machupicchureservations.org/tour/salkantay-trek-3-days#itinerary" target="_blank" style="text-decoration: none; color: #20B2AA; font-weight: bold; padding: 8px 16px; border: 2px solid #20B2AA; border-radius: 5px;">FULL ITINERARY</a></p>
        
        <ul style="margin-left: 40px; color: #333;">
            <li><strong>Day 01:</strong><br>
                  • <span style="color: #ADFF2F;">Meals:</span> Breakfast, Lunch, Tea, Dinner<br>
                  • <span style="color: #ADFF2F;">Accommodation:</span> Star Domes<br>
                  • <span style="color: #ADFF2F;">Distance:</span> 22 km (~9 hrs)<br>
                  • <span style="color: #ADFF2F;">Max Altitude:</span> 4,650 m<br>
                  • <span style="color: #ADFF2F;">Campsite:</span> 2,000 m (Lucmabamba)<br>
                  • <span style="color: #ADFF2F;">Weather:</span> Warm, windy day; cold night<br>
                  • <span style="color: #ADFF2F;">Note:</span> Conquer the trek’s highest point.
            </li>
            <li><strong>Day 02:</strong><br>
                  • <span style="color: #ADFF2F;">Meals:</span> Breakfast, Lunch, Dinner<br>
                  • <span style="color: #ADFF2F;">Accommodation:</span> Hotel in Aguas Calientes<br>
                  • <span style="color: #ADFF2F;">Difficulty:</span> Challenging<br>
                  • <span style="color: #ADFF2F;">Distance:</span> 24 km (~15 miles)<br>
                  • <span style="color: #ADFF2F;">Duration:</span> 8-9 hours<br>
                  • <span style="color: #ADFF2F;">Max Altitude:</span> 2,700 m (Llactapata)<br>
                  • <span style="color: #ADFF2F;">Town Altitude:</span> 2,000 m<br>
                  • <span style="color: #ADFF2F;">Weather:</span> Hot
            </li>
            <li><strong>Day 03 - Machu Picchu & Car Return:</strong><br>
                  • <span style="color: #ADFF2F;">Meals:</span> Breakfast<br>
                  • <span style="color: #ADFF2F;">Schedule:</span> Rise at 4:00 am; hike (1.5 hrs) or bus ($12, 30 min) to Machu Picchu<br>
                  • <span style="color: #ADFF2F;">Arrival:</span> 6:00 am; show tickets/passports<br>
                  • <span style="color: #ADFF2F;">Activities:</span> 2.5-hr guided tour (Circuit 01/02 preferred)<br>
                  • <span style="color: #ADFF2F;">Return:</span> Hike to Hidroeléctrica (3-3.5 hrs, leave 10:30 am); car to Cusco (2:30 pm, 6 hrs, arrive ~9:30 pm)<br>
            </li>
        </ul>
        """

        if self.datos['balance'] > 0:
            contenido += f"""
            <p class="block header">PAYMENT DETAILS:</p>
            <p style="color: #333;">Outstanding Balance: ${self.datos['balance']}. Pay online via WeTravel (2.9% fee) or in-person at our Cusco office (cash: no fee; card: 3.9% fee) before the briefing.</p>
            <p style="font-weight: bold; color: #FF4500;">IMPORTANT: Pay up to one day before the briefing.</p>
            """

        contenido += f"""
                <div style="border-left: 4px solid #ffaa00; padding-left: 15px; margin-top: 20px;">
            <p class="block important">OFFICE LOCATION 📍:</p>
            <ul style="margin-left: 40px; color: #333; list-style-type: none; padding-left: 0;">
                <li>Portal Nuevo 270 Plaza Regocijo - Machu Picchu Reservations:</li>
            </ul>
        </div>
        
        <p style="text-align: center;"><a href="https://maps.app.goo.gl/XcfipVKjbuLeY3no9" target="_blank" style="text-decoration: none; color: #00aaff; font-weight: bold; padding: 8px 16px; border: 2px solid #00aaff; border-radius: 5px;">👉(Google Maps)👈</a></p>

        <div style="border-left: 4px solid #ffaa00; padding-left: 15px; margin-top: 20px;">
            <p class="block important">IMPORTANT:</p>
            <p style="color: #333;">Please reply to this email with passport photos and your entry date into Peru.</p>
        </div>

        <p class="block header">DETAILS YOU SHOULD KNOW:</p>
        <ul style="margin-left: 40px; color: #333;">
            <li><strong>Maximum 3 hours allowed inside Machu Picchu</strong> per park rules.</li>
            <li><strong>Bus tickets to Machu Picchu ($12)</strong> can be arranged the night before or the morning of your visit.</li>
            <li><strong>Depart Machu Picchu by 11:30 AM</strong> to catch the car to Cusco at <strong>Hidroelectrica at 2:30 PM.</strong></li>
            <li>We do not provide transportation for the briefing session. If you cannot arrive at the office on the indicated day or time, please contact 
                <a href="https://wa.me/51908851429" target="_blank"><strong>+51 908 851 429</strong></a> to receive your briefing. <strong>We recommend patience when waiting for your call to be answered.</strong> Attending the briefing session in person is strongly preferred; phone briefings are for exceptional cases like flight delays or health issues.</li>
            <li>For <strong>changes, cancellations, or to add more members</strong> to your reservation, please send a formal email to 
                <a href="https://mail.google.com/mail/?view=cm&fs=1&to=MACHUPICCHURESERVATIONS@GMAIL.COM" target="_blank"><strong>MACHUPICCHURESERVATIONS@GMAIL.COM</strong></a> with the <strong>reason for the change or cancellation attached.</strong></li>
            <li>If you wish to add <strong>trekking poles or sleeping bags</strong>, you must do so on the day of your briefing session.</li>
            <li>We do not provide <strong>private transportation</strong> for luggage or transfers within Cusco.</li>
        </ul>

        <p style="color: #333; margin-top: 20px;">If you have any questions or need assistance, please contact <a href="https://wa.me/51908851429" 
        style="color: #ff5555; font-weight: bold;">👉MPR👈</a>. Contact us by phone call or WhatsApp message for more information or to clarify your doubts.</p>

        <div style="color: #333; font-size: 12px; margin-top: 20px;">
            <h2 style="color: #00aaff; font-size: 16px;">MACHUPICCHU RESERVATIONS</h2>
            <p><strong>Schedule:</strong> 7:00-22:00 hrs, Mon-Sat<br><strong>WhatsApp:</strong> <a href="https://api.whatsapp.com/send/?phone=51908851429" style="color: #ff5555; font-weight: bold;">👉MPR👈</a></p>
        </div>
        """

        self.mostrar_confirmacion_en_html(contenido)

    def mostrar_confirmacion_en_html(self, contenido, nombre_archivo="confirmacion.html"):
        with open(nombre_archivo, "w", encoding="utf-8") as file:
            file.write(f"""
            <html>
            <head>
                <title>Confirmación de Reserva</title>
                <style>
                    body {{ font-family: 'Verdana', sans-serif; margin: 20px; color: #333; }}
                    p {{ line-height: 1.6; font-size: 14px; }}
                    ul {{ list-style-type: none; padding-left: 0; }}
                    ul li::before {{ content: "•"; color: #ADFF2F; font-weight: bold; display: inline-block; width: 1em; margin-left: -1em; }}
                    .important {{ font-weight: bold; color: #FFA500; }}
                    .header {{ font-size: 16px; font-weight: bold; color: #20B2AA; }}
                </style>
            </head>
            <body>
                {contenido}
            </body>
            </html>
            """)
        print(f"Confirmación guardada como {nombre_archivo}")

class Salkantay2D:
    def __init__(self, datos):
        self.datos = datos

    def generar_confirmacion(self):
        tour = 'SALKANTAY PASS + HUMANTAY LAKE 2D-1N'
        tour_dias = 1
        briefing_hora = "7:00 pm"
        primer_nombre = self.datos['nombres'][0].split()[0].capitalize()

        contenido = f"""
        <p style="color: #333;">Dear {primer_nombre},</p>
        <p style="color: #333;">Your reservation is confirmed - <span style="color: #DA70D6; font-weight: bold;">{tour}</span></p>
        
        <table>
            <tr>
                <td style="font-weight: bold; color: #DA70D6;">START DATE:</td>
                <td style="color: #333;">{fecha_nombre(self.datos['fecha'][0], self.datos['fecha'][1], self.datos['fecha'][2])}</td>
            </tr>
            <tr>
                <td style="font-weight: bold; color: #DA70D6;">RETURN DATE:</td>
                <td style="color: #333;">{fecha_nombre(self.datos['fecha'][0], self.datos['fecha'][1], self.datos['fecha'][2], tour_dias)}</td>
            </tr>
            <tr>
                <td style="font-weight: bold; color: #FF6347;">BRIEFING DATE:</td>
                <td style="color: #333;">{fecha_nombre(self.datos['fecha'][0], self.datos['fecha'][1], self.datos['fecha'][2], -1)}, at {briefing_hora} at Machu Picchu Reservations.</td>
            </tr>
            <tr>
                <td style="font-weight: bold; color: #DA70D6;">N° PERSON:</td>
                <td style="color: #333;">{len(self.datos['nombres']):02}</td>
            </tr>
        </table>

        <ul style="margin-left: 40px; color: #333;">
            {''.join([f"<li>{i+1}. {nombre.strip().upper()}</li>" for i, nombre in enumerate(self.datos['nombres'])])}
        </ul>

        <p class="block header">WHAT IS INCLUDED:</p>
        <ul style="margin-left: 40px;">
            <li>Transportation: Includes transportation to the trailhead and transfers after the trail from Soraypampa to Cusco</li>
            <li>Meals: Enjoy 2 breakfasts, 2 lunches, and 1 dinner throughout your journey</li>
            <li>1 Night of accommodations: A night in comfort.</li>
            <li>Support Team: Professional guides, chefs, and assistants</li>
            <li>A professional Guide: A dedicated professional guide will accompany you throughout your journey, ensuring a memorable experience</li>
        </ul>
        """
        if self.datos.get('sleeping_bags', 0) > 0:
            contenido += f"<li>{self.datos['sleeping_bags']} Sleeping bags</li>"
        if self.datos.get('trekking_poles', 0) > 0:
            contenido += f"<li>{self.datos['trekking_poles']} Pair of Trekking poles</li>"

        contenido += f"""
        <p class="block header">WHAT TO PACK:</p>
        <ul style="margin-left: 40px; color: #333;">
            <li><strong>Clothing:</strong> Wool hat/beanie, t-shirt, layer (fleece/sweatshirt), waterproof jacket (or rain poncho), hiking pants, hiking shoes/sneakers, sunglasses, gloves.</li>
            <li><strong>Accessories:</strong> Small backpack (for water, snacks, camera).</li>
            <li><strong>Essentials:</strong> Water (2L min.), snacks (apples, cereal bars, sweets, chocolates), sunscreen, rain poncho.</li>
            <li><strong>Optional:</strong> Trekking poles (rentable), headlamp/flashlight, camera/charger.</li>
            <li><strong>Note:</strong> Use a waterproof bag; layer clothing for variable weather.</li>
        </ul>

        <p class="block header">ITINERARY SUMMARY:</p>
        <p style="text-align: center;"><a href="https://www.machupicchureservations.org/tour/salkantay-hike-2-days#itinerary" target="_blank" style="text-decoration: none; color: #DA70D6; font-weight: bold; padding: 8px 16px; border: 2px solid #DA70D6; border-radius: 5px;">FULL ITINERARY</a></p>
        
        <ul style="margin-left: 40px; color: #333;">
            <li><strong>Day 01 - Cusco to Humantay Lake & Quiswarniyoc:</strong><br>
                  • <span style="color: #FFA07A;">Start:</span> Pick-up 4:30-5:00 am from Cusco hotels or 5:00 am at office<br>
                  • <span style="color: #FFA07A;">Travel:</span> 2-hr drive to Mollepata; breakfast; 1-hr drive to Soraypampa<br>
                  • <span style="color: #FFA07A;">Hike:</span> 2-hr uphill to Humantay Lake; explore and descend 2 hrs<br>
                  • <span style="color: #FFA07A;">Camp:</span> Quiswarniyoc (4,000 m) - Crystal Igloos<br>
                  • <span style="color: #FFA07A;">Meals:</span> Breakfast, Lunch, Dinner<br>
                  • <span style="color: #FFA07A;">Optional:</span> Hike to Salkantay Mirador<br>
                  • <span style="color: #FFA07A;">Note:</span> Enjoy mountain views, llamas, and waterfalls.
            </li>
            <li><strong>Day 02 - Salkantay Pass to Cusco:</strong><br>
                  • <span style="color: #FFA07A;">Start:</span> Wake at 5:00 am with coca tea; breakfast at 5:45 am<br>
                  • <span style="color: #FFA07A;">Hike:</span> 3-4 hr uphill to Salkantay Pass (4,630 m); 2.5-hr descent to Soraypampa<br>
                  • <span style="color: #FFA07A;">Activities:</span> Mountain views, Andean ritual at summit<br>
                  • <span style="color: #FFA07A;">Travel:</span> Drive to Mollepata for lunch; 2-hr drive to Cusco (~6:00 pm)<br>
                  • <span style="color: #FFA07A;">Meals:</span> Breakfast, Lunch<br>
                  • <span style="color: #FFA07A;">Note:</span> Highest point of the trek with stunning views.
            </li>
        </ul>
        """

        if self.datos['balance'] > 0:
            contenido += f"""
            <p class="block header">PAYMENT DETAILS:</p>
            <p style="color: #333;">Outstanding Balance: ${self.datos['balance']}. Pay online via WeTravel (2.9% fee) or in-person at our Cusco office (cash: no fee; card: 3.9% fee) before the briefing.</p>
            <p style="font-weight: bold; color: #FF69B4;">IMPORTANT: Pay up to one day before the briefing.</p>
            """

        contenido += f"""
                <div style="border-left: 4px solid #ffaa00; padding-left: 15px; margin-top: 20px;">
            <p class="block important">OFFICE LOCATION 📍:</p>
            <ul style="margin-left: 40px; color: #333; list-style-type: none; padding-left: 0;">
                <li>Portal Nuevo 270 Plaza Regocijo - Machu Picchu Reservations:</li>
            </ul>
        </div>
        
        <p style="text-align: center;"><a href="https://maps.app.goo.gl/XcfipVKjbuLeY3no9" target="_blank" style="text-decoration: none; color: #00aaff; font-weight: bold; padding: 8px 16px; border: 2px solid #00aaff; border-radius: 5px;">👉(Google Maps)👈</a></p>

        <div style="border-left: 4px solid #98FB98; padding-left: 15px; margin-top: 20px;">
            <p class="block important">IMPORTANT:</p>
            <p style="color: #333;">Please reply to this email with passport photos and your entry date into Peru.</p>
        </div>

        <p class="block header">DETAILS YOU SHOULD KNOW:</p>
        <ul style="margin-left: 40px; color: #333;">
            <li>Entrance fee to Humantay Lake (20 soles, paid on-site) not included.</li>
            <li>Travel insurance and extra expenses not covered.</li>
            <li>Vegetarian/vegan meals available on request at no extra charge.</li>
        </ul>

        <p style="color: #333; margin-top: 20px;">If you have any questions or need assistance, please contact <a href="https://wa.me/51908851429" 
        style="color: #FF6347; font-weight: bold;">👉MPR👈</a>. Contact for additional info or options.</p>

        <div style="color: #333; font-size: 12px; margin-top: 20px;">
            <h2 style="color: #DA70D6; font-size: 16px;">MACHUPICCHU RESERVATIONS</h2>
            <p><strong>Schedule:</strong> 7:00-22:00 hrs, Mon-Sat<br><strong>WhatsApp:</strong> <a href="https://api.whatsapp.com/send/?phone=51908851429" style="color: #FF6347; font-weight: bold;">👉MPR👈</a></p>
        </div>
        """

        self.mostrar_confirmacion_en_html(contenido)

    def mostrar_confirmacion_en_html(self, contenido):
        nombre_archivo = "confirmacion.html"
        with open(nombre_archivo, "w", encoding="utf-8") as file:
            file.write(f"""
            <html>
            <head>
                <title>Confirmación de Reserva</title>
                <style>
                    body {{ font-family: 'Verdana', sans-serif; margin: 20px; color: #333; }}
                    p {{ line-height: 1.6; font-size: 14px; }}
                    ul {{ list-style-type: none; padding-left: 0; }}
                    ul li::before {{ content: "•"; color: #FFA07A; font-weight: bold; display: inline-block; width: 1em; margin-left: -1em; }}
                    .important {{ font-weight: bold; color: #FF6347; }}
                    .header {{ font-size: 16px; font-weight: bold; color: #DA70D6; }}
                </style>
            </head>
            <body>
                {contenido}
            </body>
            </html>
            """)
        print(f"Confirmación guardada como {nombre_archivo}")

class Llactapata3DTrain:
    def __init__(self, datos):
        self.datos = datos

    def generar_confirmacion(self):
        tour = 'LLACTAPATA TREK TO MACHU PICCHU 3D-2N'
        tour_dias = 2
        briefing_hora = "7:00 pm"
        primer_nombre = self.datos['nombres'][0].split()[0].capitalize()

        contenido = f"""
        <p style="color: #333;">Dear {primer_nombre},</p>
        <p style="color: #333;">Your reservation is confirmed - <span style="color: #6A5ACD; font-weight: bold;">{tour}</span></p>
        
        <table>
            <tr>
                <td style="font-weight: bold; color: #6A5ACD;">START DATE:</td>
                <td style="color: #333;">{fecha_nombre(self.datos['fecha'][0], self.datos['fecha'][1], self.datos['fecha'][2])}</td>
            </tr>
            <tr>
                <td style="font-weight: bold; color: #6A5ACD;">RETURN DATE:</td>
                <td style="color: #333;">{fecha_nombre(self.datos['fecha'][0], self.datos['fecha'][1], self.datos['fecha'][2], tour_dias)}</td>
            </tr>
            <tr>
                <td style="font-weight: bold; color: #DC143C;">BRIEFING DATE:</td>
                <td style="color: #333;">{fecha_nombre(self.datos['fecha'][0], self.datos['fecha'][1], self.datos['fecha'][2], -1)}, at {briefing_hora} at Machu Picchu Reservations.</td>
            </tr>
            <tr>
                <td style="font-weight: bold; color: #6A5ACD;">N° PERSON:</td>
                <td style="color: #333;">{len(self.datos['nombres']):02}</td>
            </tr>
        </table>

        <ul style="margin-left: 40px; color: #333;">
            {''.join([f"<li>{i+1}. {nombre.strip().upper()}</li>" for i, nombre in enumerate(self.datos['nombres'])])}
        </ul>

        <p class="block header">TOUR INCLUSIONS:</p>
        <ul style="margin-left: 40px;">
            <li>Transportation from Cusco to Santa Teresa town</li>
            <li>2 breakfasts</li>
            <li>2 lunches</li>
            <li>2 dinners</li>
            <li>1 comfortable night</li>
            <li>1-night hostel in Aguas Calientes</li>
        """

        if self.datos['machu_picchu_code'] == "0":
            contenido += "<li style='color: #FF4500;'>NOT INCLUDED: Entrance for MACHU PICCHU</li>"
        else:
            contenido += f"<li>Entrance for MACHU PICCHU</li>"
            contenido += f"<li>MACHU PICCHU CODES: {self.datos['machu_picchu_code']}</li>"

        if self.datos.get('montaña', '0') != '0':
            contenido += f"<li>Entrance for {self.datos['montaña']}</li>"

        if self.datos.get("vistadome_retorno", False):
            contenido += "<li>Train from Aguas Calientes to Ollantaytambo - BY TRAIN VISTADOME</li>"
        else:
            contenido += "<li>Train from Aguas Calientes to Ollantaytambo - BY TRAIN</li>"

        contenido += "<li>Transfer from Ollantaytambo to Cusco</li>"

        if self.datos.get('sleeping_bags', 0) > 0:
            contenido += f"<li>{self.datos['sleeping_bags']} Sleeping bags rental</li>"
        if self.datos.get('trekking_poles', 0) > 0:
            contenido += f"<li>{self.datos['trekking_poles']} Trekking poles rental (pair)</li>"
        
        contenido += f"<li>{len(self.datos['nombres']):02} Zipline participants</li>"

        contenido += """
            <li>Guide</li>
            <li>Cooks</li>
        </ul>

        <p class="block header">WHAT TO PACK:</p>
        <ul style="margin-left: 40px; color: #333;">
            <li><strong>Essentials:</strong> Backpack, sleeping bag (-5°C, rentable), trekking poles (optional, rentable), water bottle, sunscreen, insect repellent, toiletries, toilet paper.</li>
            <li><strong>Clothing:</strong> Wool hat/cap, sun hat, 1-2 long-sleeve t-shirts, long pants/leggings, hiking shoes, 1-2 pairs wool socks, rain gear (jacket/pants/poncho), shorts, sandals/flip-flops, bathing suit.</li>
            <li><strong>Extras:</strong> Small towel, sunglasses, snacks (chocolate, cereal bars, etc.), extra money in Soles.</li>
            <li><strong>Documents:</strong> Original passport, student ID (if applicable).</li>
            <li><strong>Note:</strong> 7kg duffle bag provided, carried by horses.</li>
        </ul>

        <p class="block header">ITINERARY SUMMARY:</p>
        <p style="text-align: center;"><a href="https://www.machupicchureservations.org/tour/llactapata-trek-3-days#itinerary" target="_blank" style="text-decoration: none; color: #6A5ACD; font-weight: bold; padding: 8px 16px; border: 2px solid #6A5ACD; border-radius: 5px;">FULL ITINERARY</a></p>
        
        <ul style="margin-left: 40px; color: #333;">
            <li><strong>Day 01 - Cusco to Santa Teresa:</strong><br>
                  • <span style="color: #40E0D0;">Start:</span> 6:30 AM at Machu Picchu Reservations office<br>
                  • <span style="color: #40E0D0;">Travel:</span> 5-hr drive to Santa Teresa; lunch at 1:00 PM<br>
                  • <span style="color: #40E0D0;">Activities:</span> 30-min ride to Lucmabamba; 1.5-2 hr zipline (5 cables, Tibetan bridge); 30-min drive to Cocalmayo Hot Springs (2 hrs)<br>
                  • <span style="color: #40E0D0;">Stay:</span> 45-min drive to Star Domes (overnight)<br>
                  • <span style="color: #40E0D0;">Meals:</span> Lunch, Dinner
            </li>
            <li><strong>Day 02 - Lucmabamba to Aguas Calientes:</strong><br>
                  • <span style="color: #40E0D0;">Start:</span> Wake at 5:30 AM; breakfast at 6:00 AM<br>
                  • <span style="color: #40E0D0;">Activities:</span> 30-45 min coffee tour; 3-hr uphill hike to Llactapata ruins (12 km); 2-hr downhill to Hidroeléctrica<br>
                  • <span style="color: #40E0D0;">Hike:</span> 3-hr flat walk to Aguas Calientes<br>
                  • <span style="color: #40E0D0;">Stay:</span> Hotel in Aguas Calientes<br>
                  • <span style="color: #40E0D0;">Meals:</span> Breakfast, Lunch, Dinner (7:00 PM)
            </li>
            <li><strong>Day 03 - Machu Picchu & Train Return:</strong><br>
                  • <span style="color: #40E0D0;">Start:</span> Wake at 4:00 AM; breakfast; hike (1.5 hrs) or bus ($12, 30 min) to Machu Picchu<br>
                  • <span style="color: #40E0D0;">Arrival:</span> 6:00 AM; show tickets/passports<br>
                  • <span style="color: #40E0D0;">Activities:</span> 2.5-hr guided tour (Circuit 01/02 preferred); optional Huayna Picchu/Machu Picchu Mountain ($60, pre-booked)<br>
                  • <span style="color: #40E0D0;">Return:</span> Walk (1.5 hrs) or bus ($12) to Aguas Calientes; train to Ollantaytambo (2:30/2:55 PM, 1.5 hrs); car to Cusco (2 hrs, ~6:30 PM)<br>
                  • <span style="color: #40E0D0;">Meals:</span> Breakfast<br>
                  • <span style="color: #40E0D0;">Note:</span> Train return recommended for mountain hikes.
            </li>
        </ul>
        """

        if self.datos['balance'] > 0:
            contenido += f"""
            <p class="block header">PAYMENT DETAILS:</p>
            <p style="color: #333;">Outstanding Balance: ${self.datos['balance']}. Pay online via WeTravel (2.9% fee) or in-person at our Cusco office (cash: no fee; card: 3.9% fee) before the briefing.</p>
            <p style="font-weight: bold; color: #FF00FF;">IMPORTANT: Pay up to one day before the briefing.</p>
            """

        contenido += f"""
                <div style="border-left: 4px solid #ffaa00; padding-left: 15px; margin-top: 20px;">
            <p class="block important">OFFICE LOCATION 📍:</p>
            <ul style="margin-left: 40px; color: #333; list-style-type: none; padding-left: 0;">
                <li>Portal Nuevo 270 Plaza Regocijo - Machu Picchu Reservations:</li>
            </ul>
        </div>
        
        <p style="text-align: center;"><a href="https://maps.app.goo.gl/XcfipVKjbuLeY3no9" target="_blank" style="text-decoration: none; color: #00aaff; font-weight: bold; padding: 8px 16px; border: 2px solid #00aaff; border-radius: 5px;">👉(Google Maps)👈</a></p>

        <div style="border-left: 4px solid #FFB6C1; padding-left: 15px; margin-top: 20px;">
            <p class="block important">IMPORTANT:</p>
            <p style="color: #333;">Please reply to this email with passport photos and your entry date into Peru.</p>
        </div>

        <p class="block header">DETAILS YOU SHOULD KNOW:</p>
        <ul style="margin-left: 40px; color: #333;">
            <li><strong>Maximum 3 hours allowed inside Machu Picchu</strong> per park rules.</li>
            <li><strong>Bus tickets to Machu Picchu ($12)</strong> can be arranged the night before or the morning of your visit.</li>
            <li>We do not provide transportation for the briefing session. If you cannot arrive at the office on the indicated day or time, please contact 
                <a href="https://wa.me/51908851429" target="_blank"><strong>+51 908 851 429</strong></a> to receive your briefing. <strong>We recommend patience when waiting for your call to be answered.</strong> Attending the briefing session in person is strongly preferred; phone briefings are for exceptional cases like flight delays or health issues.</li>
            <li>For changes, cancellations, or to add more members to your reservation, please send a formal email to 
                <a href="https://mail.google.com/mail/?view=cm&fs=1&to=MACHUPICCHURESERVATIONS@GMAIL.COM" target="_blank"><strong>MACHUPICCHURESERVATIONS@GMAIL.COM</strong></a> with the <strong>reason for the change or cancellation attached.</strong></li>
            <li>If you wish to add <strong>trekking poles or sleeping bags</strong>, you must do so on the day of your briefing session.</li>
            <li>We do not provide <strong>private transportation</strong> for luggage or transfers within Cusco.</li>
            <li><strong>Train times may vary slightly;</strong> confirm at briefing.</li>
        </ul>

        <p style="color: #333; margin-top: 20px;">If you have any questions or need assistance, please contact <a href="https://wa.me/51908851429" 
        style="color: #DC143C; font-weight: bold;">👉MPR👈</a>. Contact for additional info or options.</p>

        <div style="color: #333; font-size: 12px; margin-top: 20px;">
            <h2 style="color: #6A5ACD; font-size: 16px;">MACHUPICCHU RESERVATIONS</h2>
            <p><strong>Schedule:</strong> 7:00-22:00 hrs, Mon-Sat<br><strong>WhatsApp:</strong> <a href="https://api.whatsapp.com/send/?phone=51908851429" style="color: #DC143C; font-weight: bold;">👉MPR👈</a></p>
        </div>
        """

        self.mostrar_confirmacion_en_html(contenido)

    def mostrar_confirmacion_en_html(self, contenido):
        nombre_archivo = "confirmacion.html"
        with open(nombre_archivo, "w", encoding="utf-8") as file:
            file.write(f"""
            <html>
            <head>
                <title>Confirmación de Reserva</title>
                <style>
                    body {{ font-family: 'Verdana', sans-serif; margin: 20px; color: #333; }}
                    p {{ line-height: 1.6; font-size: 14px; }}
                    ul {{ list-style-type: none; padding-left: 0; }}
                    ul li::before {{ content: "•"; color: #40E0D0; font-weight: bold; display: inline-block; width: 1em; margin-left: -1em; }}
                    .important {{ font-weight: bold; color: #DC143C; }}
                    .header {{ font-size: 16px; font-weight: bold; color: #6A5ACD; }}
                </style>
            </head>
            <body>
                {contenido}
            </body>
            </html>
            """)
        print(f"Confirmación guardada como {nombre_archivo}")

class Llactapata3DCar:
    def __init__(self, datos):
        self.datos = datos

    def generar_confirmacion(self):
        tour = 'LLACTAPATA TREK TO MACHU PICCHU 3D-2N'
        tour_dias = 2
        briefing_hora = "7:00 pm"
        primer_nombre = self.datos['nombres'][0].split()[0].capitalize()

        contenido = f"""
        <p style="color: #333;">Dear {primer_nombre},</p>
        <p style="color: #333;">Your reservation is confirmed - <span style="color: #6A5ACD; font-weight: bold;">{tour}</span></p>
        
        <table>
            <tr>
                <td style="font-weight: bold; color: #6A5ACD;">START DATE:</td>
                <td style="color: #333;">{fecha_nombre(self.datos['fecha'][0], self.datos['fecha'][1], self.datos['fecha'][2])}</td>
            </tr>
            <tr>
                <td style="font-weight: bold; color: #6A5ACD;">RETURN DATE:</td>
                <td style="color: #333;">{fecha_nombre(self.datos['fecha'][0], self.datos['fecha'][1], self.datos['fecha'][2], tour_dias)}</td>
            </tr>
            <tr>
                <td style="font-weight: bold; color: #DC143C;">BRIEFING DATE:</td>
                <td style="color: #333;">{fecha_nombre(self.datos['fecha'][0], self.datos['fecha'][1], self.datos['fecha'][2], -1)}, at {briefing_hora} at Machu Picchu Reservations.</td>
            </tr>
            <tr>
                <td style="font-weight: bold; color: #6A5ACD;">N° PERSON:</td>
                <td style="color: #333;">{len(self.datos['nombres']):02}</td>
            </tr>
        </table>

        <ul style="margin-left: 40px; color: #333;">
            {''.join([f"<li>{i+1}. {nombre.strip().upper()}</li>" for i, nombre in enumerate(self.datos['nombres'])])}
        </ul>

        <p class="block header">TOUR INCLUSIONS:</p>
        <ul style="margin-left: 40px;">
            <li>Transportation from Cusco to Santa Teresa town</li>
            <li>2 breakfasts</li>
            <li>2 lunches</li>
            <li>2 dinners</li>
            <li>1 comfortable night</li>
            <li>1-night hostel in Aguas Calientes</li>
        """

        if self.datos['machu_picchu_code'] == "0":
            contenido += "<li style='color: #FF4500;'>NOT INCLUDED: Entrance for MACHU PICCHU</li>"
        else:
            contenido += f"<li>Entrance for MACHU PICCHU</li>"
            contenido += f"<li>MACHU PICCHU CODES: {self.datos['machu_picchu_code']}</li>"

        contenido += "<li>Transportation from Hidroeléctrica to Cusco - BY CAR</li>"

        if self.datos.get('sleeping_bags', 0) > 0:
            contenido += f"<li>{self.datos['sleeping_bags']} Sleeping bags rental</li>"
        if self.datos.get('trekking_poles', 0) > 0:
            contenido += f"<li>{self.datos['trekking_poles']} Trekking poles rental (pair)</li>"

        contenido += f"<li>{len(self.datos['nombres']):02} Zipline participants</li>"

        contenido += """
            <li>Guide</li>
            <li>Cooks</li>
        </ul>

        <p class="block header">WHAT TO PACK:</p>
        <ul style="margin-left: 40px; color: #333;">
            <li><strong>Essentials:</strong> Backpack, sleeping bag (-5°C, rentable), trekking poles (optional, rentable), water bottle, sunscreen, insect repellent, toiletries, toilet paper.</li>
            <li><strong>Clothing:</strong> Wool hat/cap, sun hat, 1-2 long-sleeve t-shirts, long pants/leggings, hiking shoes, 1-2 pairs wool socks, rain gear (jacket/pants/poncho), shorts, sandals/flip-flops, bathing suit.</li>
            <li><strong>Extras:</strong> Small towel, sunglasses, snacks (chocolate, cereal bars, etc.), extra money in Soles.</li>
            <li><strong>Documents:</strong> Original passport, student ID (if applicable).</li>
            <li><strong>Note:</strong> 7kg duffle bag provided, carried by horses.</li>
        </ul>

        <p class="block header">ITINERARY SUMMARY:</p>
        <p style="text-align: center;"><a href="https://www.machupicchureservations.org/tour/llactapata-trek-3-days#itinerary" target="_blank" style="text-decoration: none; color: #6A5ACD; font-weight: bold; padding: 8px 16px; border: 2px solid #6A5ACD; border-radius: 5px;">FULL ITINERARY</a></p>
        
        <ul style="margin-left: 40px; color: #333;">
            <li><strong>Day 01 - Cusco to Santa Teresa:</strong><br>
                  • <span style="color: #40E0D0;">Start:</span> 6:30 AM at Machu Picchu Reservations office<br>
                  • <span style="color: #40E0D0;">Travel:</span> 5-hr drive to Santa Teresa; lunch at 1:00 PM<br>
                  • <span style="color: #40E0D0;">Activities:</span> 30-min ride to Lucmabamba; 1.5-2 hr zipline (5 cables, Tibetan bridge); 30-min drive to Cocalmayo Hot Springs (2 hrs)<br>
                  • <span style="color: #40E0D0;">Stay:</span> 45-min drive to Star Domes (overnight)<br>
                  • <span style="color: #40E0D0;">Meals:</span> Lunch, Dinner
            </li>
            <li><strong>Day 02 - Lucmabamba to Aguas Calientes:</strong><br>
                  • <span style="color: #40E0D0;">Start:</span> Wake at 5:30 AM; breakfast at 6:00 AM<br>
                  • <span style="color: #40E0D0;">Activities:</span> 30-45 min coffee tour; 3-hr uphill hike to Llactapata ruins (12 km); 2-hr downhill to Hidroeléctrica<br>
                  • <span style="color: #40E0D0;">Hike:</span> 3-hr flat walk to Aguas Calientes<br>
                  • <span style="color: #40E0D0;">Stay:</span> Hotel in Aguas Calientes<br>
                  • <span style="color: #40E0D0;">Meals:</span> Breakfast, Lunch, Dinner (7:00 PM)
            </li>
            <li><strong>Day 03 - Machu Picchu & Car Return:</strong><br>
                  • <span style="color: #40E0D0;">Start:</span> Wake at 4:00 AM; breakfast; hike (1.5 hrs) or bus ($12, 30 min) to Machu Picchu<br>
                  • <span style="color: #40E0D0;">Arrival:</span> 6:00 AM; show tickets/passports<br>
                  • <span style="color: #40E0D0;">Activities:</span> 2.5-hr guided tour (Circuit 01/02 preferred)<br>
                  • <span style="color: #40E0D0;">Return:</span> Hike to Hidroeléctrica (3-3.5 hrs, leave 10:30 AM); car to Cusco (2:30 PM, 6 hrs, ~9:30 PM)<br>
                  • <span style="color: #40E0D0;">Meals:</span> Breakfast<br>
            </li>
        </ul>
        """

        if self.datos['balance'] > 0:
            contenido += f"""
            <p class="block header">PAYMENT DETAILS:</p>
            <p style="color: #333;">Outstanding Balance: ${self.datos['balance']}. Pay online via WeTravel (2.9% fee) or in-person at our Cusco office (cash: no fee; card: 3.9% fee) before the briefing.</p>
            <p style="font-weight: bold; color: #FF00FF;">IMPORTANT: Pay up to one day before the briefing.</p>
            """

        contenido += f"""
                <div style="border-left: 4px solid #ffaa00; padding-left: 15px; margin-top: 20px;">
            <p class="block important">OFFICE LOCATION 📍:</p>
            <ul style="margin-left: 40px; color: #333; list-style-type: none; padding-left: 0;">
                <li>Portal Nuevo 270 Plaza Regocijo - Machu Picchu Reservations:</li>
            </ul>
        </div>
        
        <p style="text-align: center;"><a href="https://maps.app.goo.gl/XcfipVKjbuLeY3no9" target="_blank" style="text-decoration: none; color: #00aaff; font-weight: bold; padding: 8px 16px; border: 2px solid #00aaff; border-radius: 5px;">👉(Google Maps)👈</a></p>

        <div style="border-left: 4px solid #FFB6C1; padding-left: 15px; margin-top: 20px;">
            <p class="block important">IMPORTANT:</p>
            <p style="color: #333;">Please reply to this email with passport photos and your entry date into Peru.</p>
        </div>

        <p class="block header">DETAILS YOU SHOULD KNOW:</p>
        <ul style="margin-left: 40px; color: #333;">
            <li><strong>Maximum 3 hours allowed inside Machu Picchu</strong> per park rules.</li>
            <li><strong>Bus tickets to Machu Picchu ($12)</strong> can be arranged the night before or the morning of your visit.</li>
            <li><strong>Depart Machu Picchu by 11:30 AM</strong> to catch the car to Cusco at <strong>Hidroelectrica at 2:30 PM.</strong></li>
            <li>We do not provide transportation for the briefing session. If you cannot arrive at the office on the indicated day or time, please contact 
                <a href="https://wa.me/51908851429" target="_blank"><strong>+51 908 851 429</strong></a> to receive your briefing. <strong>We recommend patience when waiting for your call to be answered.</strong> Attending the briefing session in person is strongly preferred; phone briefings are for exceptional cases like flight delays or health issues.</li>
            <li>For <strong>changes, cancellations, or to add more members</strong> to your reservation, please send a formal email to 
                <a href="https://mail.google.com/mail/?view=cm&fs=1&to=MACHUPICCHURESERVATIONS@GMAIL.COM" target="_blank"><strong>MACHUPICCHURESERVATIONS@GMAIL.COM</strong></a> with the <strong>reason for the change or cancellation attached.</strong></li>
            <li>If you wish to add <strong>trekking poles or sleeping bags</strong>, you must do so on the day of your briefing session.</li>
            <li>We do not provide <strong>private transportation</strong> for luggage or transfers within Cusco.</li>
        </ul>

        <p style="color: #333; margin-top: 20px;">If you have any questions or need assistance, please contact <a href="https://wa.me/51908851429" 
        style="color: #DC143C; font-weight: bold;">👉MPR👈</a>. Contact for additional info or options.</p>

        <div style="color: #333; font-size: 12px; margin-top: 20px;">
            <h2 style="color: #6A5ACD; font-size: 16px;">MACHUPICCHU RESERVATIONS</h2>
            <p><strong>Schedule:</strong> 7:00-22:00 hrs, Mon-Sat<br><strong>WhatsApp:</strong> <a href="https://api.whatsapp.com/send/?phone=51908851429" style="color: #DC143C; font-weight: bold;">👉MPR👈</a></p>
        </div>
        """

        self.mostrar_confirmacion_en_html(contenido)

    def mostrar_confirmacion_en_html(self, contenido):
        nombre_archivo = "confirmacion.html"
        with open(nombre_archivo, "w", encoding="utf-8") as file:
            file.write(f"""
            <html>
            <head>
                <title>Confirmación de Reserva</title>
                <style>
                    body {{ font-family: 'Verdana', sans-serif; margin: 20px; color: #333; }}
                    p {{ line-height: 1.6; font-size: 14px; }}
                    ul {{ list-style-type: none; padding-left: 0; }}
                    ul li::before {{ content: "•"; color: #40E0D0; font-weight: bold; display: inline-block; width: 1em; margin-left: -1em; }}
                    .important {{ font-weight: bold; color: #DC143C; }}
                    .header {{ font-size: 16px; font-weight: bold; color: #6A5ACD; }}
                </style>
            </head>
            <body>
                {contenido}
            </body>
            </html>
            """)
        print(f"Confirmación guardada como {nombre_archivo}")

class IncaTrail4D:
    def __init__(self, datos):
        self.datos = datos

    def generar_confirmacion(self):
        tour = 'INCA TRAIL TO MACHU PICCHU 4 DAYS'
        tour_dias = 3
        briefing_hora = "6:00 pm"
        primer_nombre = self.datos['nombres'][0].split()[0].capitalize()

        contenido = f"""
        <p style="color: #333;">Dear {primer_nombre},</p>
        <p style="color: #333;">Your reservation is confirmed - <span style="color: #228B22; font-weight: bold;">{tour}</span></p>
        
        <table>
            <tr>
                <td style="font-weight: bold; color: #228B22;">START DATE:</td>
                <td style="color: #333;">{fecha_nombre(self.datos['fecha'][0], self.datos['fecha'][1], self.datos['fecha'][2])}</td>
            </tr>
            <tr>
                <td style="font-weight: bold; color: #228B22;">RETURN DATE:</td>
                <td style="color: #333;">{fecha_nombre(self.datos['fecha'][0], self.datos['fecha'][1], self.datos['fecha'][2], tour_dias)}</td>
            </tr>
            <tr>
                <td style="font-weight: bold; color: #FF4500;">BRIEFING DATE:</td>
                <td style="color: #333;">{fecha_nombre(self.datos['fecha'][0], self.datos['fecha'][1], self.datos['fecha'][2], -1)}, at {briefing_hora} at Machu Picchu Reservations.</td>
            </tr>
            <tr>
                <td style="font-weight: bold; color: #228B22;">N° PERSON:</td>
                <td style="color: #333;">{len(self.datos['nombres']):02}</td>
            </tr>
        </table>

        <ul style="margin-left: 40px; color: #333;">
            {''.join([f"<li>{i+1}. {nombre.strip().upper()}</li>" for i, nombre in enumerate(self.datos['nombres'])])}
        </ul>

        <p class="block header">TOUR INCLUSIONS:</p>
        <ul style="margin-left: 40px;">
            <li>Pick up from your hotel</li>
            <li>Transportation to the trailhead</li>
            <li>4 breakfasts</li>
            <li>4 lunches</li>
            <li>3 dinners</li>
            <li>3 comfortable nights</li>
        """

        if self.datos['machu_picchu_code'] == "0":
            contenido += "<li style='color: #FF4500;'>NOT INCLUDED: Entrance for MACHU PICCHU</li>"
        else:
            contenido += f"<li>Entrance for the INCA TRAIL + MACHU PICCHU</li>"
            contenido += f"<li>MACHU PICCHU CODES: {self.datos['machu_picchu_code']}</li>"

        if self.datos.get('montaña', '0') != '0':
            contenido += f"<li>Entrance for {self.datos['montaña']}</li>"

        contenido += "<li>Bus from Machu Picchu to Aguas Calientes town</li>"

        if self.datos.get("vistadome_retorno", False):
            contenido += "<li>Train from Aguas Calientes to Ollantaytambo - BY TRAIN VISTADOME</li>"
        else:
            contenido += "<li>Train from Aguas Calientes to Ollantaytambo - BY TRAIN</li>"

        contenido += "<li>Transfer from Ollantaytambo to your hotel</li>"
        contenido += f"<li>{len(self.datos['nombres'])} porters for 7 kilos</li>"

        if self.datos.get('sleeping_bags', 0) > 0:
            contenido += f"<li>{self.datos['sleeping_bags']} Sleeping bags</li>"
        if self.datos.get('trekking_poles', 0) > 0:
            contenido += f"<li>{self.datos['trekking_poles']} Pair of Trekking poles</li>"

        contenido += """
            <li>Guide</li>
            <li>Cooks</li>
        </ul>

        <p class="block header">WHAT TO PACK:</p>
        <ul style="margin-left: 40px; color: #333;">
            <li><strong>Footwear:</strong> Hiking boots (broken-in), camp shoes/flip-flops.</li>
            <li><strong>Backpack:</strong> 20-30L daypack, rain cover (provided free).</li>
            <li><strong>Hydration:</strong> 2L water bottle/hydration system, optional purification tablets.</li>
            <li><strong>Nutrition:</strong> Snacks provided (fruit, energy bar, chocolate, candies); optional extras (nuts, etc.).</li>
            <li><strong>Clothing:</strong> Base layer (wicking t-shirts, thermals), mid layer (fleece/jacket), outer layer (waterproof jacket/pants), trekking pants, hat, gloves, extra set.</li>
            <li><strong>Protection:</strong> Sunscreen (high SPF), sunglasses, insect repellent (DEET).</li>
            <li><strong>Sleeping:</strong> Sleeping bag (-10°C, rentable), optional pillow.</li>
            <li><strong>Equipment:</strong> Trekking poles (rentable), headlamp (with batteries).</li>
            <li><strong>Personal:</strong> Toiletries, medications, small towel, first aid (blister pads).</li>
            <li><strong>Documents/Cash:</strong> Passport, permits, small cash in Soles.</li>
            <li><strong>Note:</strong> 7kg duffle bag provided, carried by porters.</li>
        </ul>

        <p class="block header">ITINERARY SUMMARY:</p>
        <p style="text-align: center;"><a href="https://www.machupicchureservations.org/tour/inca-trail-4-days#itinerary" target="_blank" style="text-decoration: none; color: #228B22; font-weight: bold; padding: 8px 16px; border: 2px solid #228B22; border-radius: 5px;">FULL ITINERARY</a></p>
        
        <ul style="margin-left: 40px; color: #333;">
            <li><strong>Day 01 - Cusco to Wayllabamba:</strong><br>
                  • <span style="color: #FFD700;">Start:</span> Pick-up 5:30-6:00 AM from Cusco hotel; 2-hr drive to Piscacucho (KM 82)<br>
                  • <span style="color: #FFD700;">Hike:</span> 8.7 miles/14 km (6-7 hrs) along Urubamba River, passing Llactapata<br>
                  • <span style="color: #FFD700;">Camp:</span> Wayllabamba (3,000 m)<br>
                  • <span style="color: #FFD700;">Meals:</span> Breakfast, Lunch, Dinner<br>
                  • <span style="color: #FFD700;">Difficulty:</span> Moderate<br>
                  • <span style="color: #FFD700;">Weather:</span> Warm, windy
            </li>
            <li><strong>Day 02 - Wayllabamba to Pacaymayo:</strong><br>
                  • <span style="color: #FFD700;">Hike:</span> 6.2 miles/10 km (6-7 hrs); steep ascent to Dead Woman’s Pass (4,215 m), descent to Pacaymayo<br>
                  • <span style="color: #FFD700;">Sites:</span> Runkurakay, Sayacmarca ruins<br>
                  • <span style="color: #FFD700;">Camp:</span> Pacaymayo (3,700 m)<br>
                  • <span style="color: #FFD700;">Meals:</span> Breakfast, Lunch, Dinner<br>
                  • <span style="color: #FFD700;">Difficulty:</span> Challenging (highest passes)<br>
                  • <span style="color: #FFD700;">Weather:</span> Cold, rainy
            </li>
            <li><strong>Day 03 - Pacaymayo to Wiñaywayna:</strong><br>
                  • <span style="color: #FFD700;">Hike:</span> 9.94 miles/16 km (7-8 hrs); climb to 3,850 m, descend to Wiñay Wayna<br>
                  • <span style="color: #FFD700;">Sites:</span> Phuyupatamarca ruins, waterfalls<br>
                  • <span style="color: #FFD700;">Camp:</span> Wiñay Wayna (2,600 m)<br>
                  • <span style="color: #FFD700;">Meals:</span> Breakfast, Lunch, Dinner<br>
                  • <span style="color: #FFD700;">Difficulty:</span> Moderate (mostly downhill)<br>
                  • <span style="color: #FFD700;">Weather:</span> Warm, humid, chilly
            </li>
            <li><strong>Day 04 - Machu Picchu & Return:</strong><br>
                  • <span style="color: #FFD700;">Start:</span> Early trek to Sun Gate; descend to Machu Picchu<br>
                  • <span style="color: #FFD700;">Activities:</span> 2.5-hr guided tour; explore ruins<br>
                  • <span style="color: #FFD700;">Return:</span> Bus to Aguas Calientes; train to Ollantaytambo (2:30/2:55 PM); car to Cusco (~6:30 PM)<br>
                  • <span style="color: #FFD700;">Meals:</span> Breakfast, Lunch<br>
                  • <span style="color: #FFD700;">Difficulty:</span> Easy, exciting<br>
                  • <span style="color: #FFD700;">Weather:</span> Hot, humid
            </li>
        </ul>
        """

        if self.datos['balance'] > 0:
            contenido += f"""
            <p class="block header">PAYMENT DETAILS:</p>
            <p style="color: #333;">Outstanding Balance: ${self.datos['balance']}. Pay online via WeTravel (2.9% fee) or in-person at our Cusco office (cash: no fee; card: 3.9% fee) before the briefing.</p>
            <p style="font-weight: bold; color: #FF1493;">IMPORTANT: Pay up to one day before the briefing.</p>
            """

        contenido += f"""
                <div style="border-left: 4px solid #ffaa00; padding-left: 15px; margin-top: 20px;">
            <p class="block important">OFFICE LOCATION 📍:</p>
            <ul style="margin-left: 40px; color: #333; list-style-type: none; padding-left: 0;">
                <li>Portal Nuevo 270 Plaza Regocijo - Machu Picchu Reservations:</li>
            </ul>
        </div>
        
        <p style="text-align: center;"><a href="https://maps.app.goo.gl/XcfipVKjbuLeY3no9" target="_blank" style="text-decoration: none; color: #00aaff; font-weight: bold; padding: 8px 16px; border: 2px solid #00aaff; border-radius: 5px;">👉(Google Maps)👈</a></p>

        <div style="border-left: 4px solid #87CEFA; padding-left: 15px; margin-top: 20px;">
            <p class="block important">IMPORTANT:</p>
            <p style="color: #333;">Please reply to this email with passport photos and your entry date into Peru.</p>
        </div>

        <p class="block header">DETAILS YOU SHOULD KNOW:</p>
        <ul style="margin-left: 40px; color: #333;">
            <li>We do not provide transportation for the briefing session. If you cannot arrive at the office on the indicated day or time, please contact 
                <a href="https://wa.me/51908851429" target="_blank"><strong>+51 908 851 429</strong></a> to receive your briefing. <strong>We recommend patience when waiting for your call to be answered.</strong> Attending the briefing session in person is strongly preferred; phone briefings are for exceptional cases like flight delays or health issues.</li>
            <li>For changes, cancellations, or to add more members to your reservation, please send a formal email to 
                <a href="https://mail.google.com/mail/?view=cm&fs=1&to=MACHUPICCHURESERVATIONS@GMAIL.COM" target="_blank"><strong>MACHUPICCHURESERVATIONS@GMAIL.COM</strong></a> with the <strong>reason for the change or cancellation attached.</strong></li>
            <li>If you wish to add <strong>trekking poles or sleeping bags</strong>, you must do so on the day of your briefing session.</li>
            <li>We do not provide <strong>private transportation</strong> for luggage or transfers within Cusco.</li>
            <li>Train times may vary; confirm at briefing.</li>
            <li>Bring extra water for Day 4 (hot, humid).</li>
        </ul>

        <p style="color: #333; margin-top: 20px;">If you have any questions or need assistance, please contact <a href="https://wa.me/51908851429" 
        style="color: #FF4500; font-weight: bold;">👉MPR👈</a>. Contact for additional info or options.</p>

        <div style="color: #333; font-size: 12px; margin-top: 20px;">
            <h2 style="color: #228B22; font-size: 16px;">MACHUPICCHU RESERVATIONS</h2>
            <p><strong>Schedule:</strong> 7:00-22:00 hrs, Mon-Sat<br><strong>WhatsApp:</strong> <a href="https://api.whatsapp.com/send/?phone=51908851429" style="color: #FF4500; font-weight: bold;">👉MPR👈</a></p>
        </div>
        """

        self.mostrar_confirmacion_en_html(contenido)

    def mostrar_confirmacion_en_html(self, contenido):
        nombre_archivo = "confirmacion.html"
        with open(nombre_archivo, "w", encoding="utf-8") as file:
            file.write(f"""
            <html>
            <head>
                <title>Confirmación de Reserva</title>
                <style>
                    body {{ font-family: 'Verdana', sans-serif; margin: 20px; color: #333; }}
                    p {{ line-height: 1.6; font-size: 14px; }}
                    ul {{ list-style-type: none; padding-left: 0; }}
                    ul li::before {{ content: "•"; color: #FFD700; font-weight: bold; display: inline-block; width: 1em; margin-left: -1em; }}
                    .important {{ font-weight: bold; color: #FF4500; }}
                    .header {{ font-size: 16px; font-weight: bold; color: #228B22; }}
                </style>
            </head>
            <body>
                {contenido}
            </body>
            </html>
            """)
        print(f"Confirmación guardada como {nombre_archivo}")

class IncaTrail2D:
    def __init__(self, datos):
        self.datos = datos

    def generar_confirmacion(self):
        tour = 'INCA TRAIL TO MACHU PICCHU 2D-1N'
        tour_dias = 1
        briefing_hora = "6:00 pm"
        primer_nombre = self.datos['nombres'][0].split()[0].capitalize()

        contenido = f"""
        <p style="color: #333;">Dear {primer_nombre},</p>
        <p style="color: #333;">Your reservation is confirmed - <span style="color: #FFA500; font-weight: bold;">{tour}</span></p>
        
        <table>
            <tr>
                <td style="font-weight: bold; color: #FFA500;">START DATE:</td>
                <td style="color: #333;">{fecha_nombre(self.datos['fecha'][0], self.datos['fecha'][1], self.datos['fecha'][2])}</td>
            </tr>
            <tr>
                <td style="font-weight: bold; color: #FFA500;">RETURN DATE:</td>
                <td style="color: #333;">{fecha_nombre(self.datos['fecha'][0], self.datos['fecha'][1], self.datos['fecha'][2], tour_dias)}</td>
            </tr>
            <tr>
                <td style="font-weight: bold; color: #20B2AA;">BRIEFING DATE:</td>
                <td style="color: #333;">{fecha_nombre(self.datos['fecha'][0], self.datos['fecha'][1], self.datos['fecha'][2], -1)}, at {briefing_hora} at Machu Picchu Reservations.</td>
            </tr>
            <tr>
                <td style="font-weight: bold; color: #FFA500;">N° PERSON:</td>
                <td style="color: #333;">{len(self.datos['nombres']):02}</td>
            </tr>
        </table>

        <ul style="margin-left: 40px; color: #333;">
            {''.join([f"<li>{i+1}. {nombre.strip().upper()}</li>" for i, nombre in enumerate(self.datos['nombres'])])}
        </ul>

        <p class="block header">TOUR INCLUSIONS:</p>
        <ul style="margin-left: 40px;">
            <li>Pick up from your hotel and drop off</li>
            <li>TRANSFER Cusco - Ollantaytambo</li>
            <li>TRAIN FROM- Ollantaytambo - KM 104</li>
            <li>01 breakfast</li>
            <li>01 lunch</li>
            <li>01 dinner</li>
            <li>1-night hotel in Aguas Calientes</li>
            <li>Bus Consettur Machu Picchu first day (OW) second day (R/T)</li>
        """

        if self.datos['machu_picchu_code'] == "0":
            contenido += "<li style='color: #FF4500;'>NOT INCLUDED: Entrance for MACHU PICCHU</li>"
        else:
            contenido += f"<li>Entrance for the INCA TRAIL + MACHU PICCHU</li>"
            contenido += f"<li>MACHU PICCHU CODES: {self.datos['machu_picchu_code']}</li>"

        if self.datos.get('montaña', '0') != '0':
            contenido += f"<li>Entrance for {self.datos['montaña']}</li>"

        if self.datos.get("vistadome_retorno", False):
            contenido += "<li>Train from Aguas Calientes to Ollantaytambo - BY TRAIN VISTADOME</li>"
        else:
            contenido += "<li>Train from Aguas Calientes to Ollantaytambo - BY TRAIN</li>"

        contenido += "<li>Transfer from Ollantaytambo to Cusco</li>"
        contenido += "<li>Tour guide</li>"

        if self.datos.get('sleeping_bags', 0) > 0:
            contenido += f"<li>{self.datos['sleeping_bags']} Sleeping bags</li>"
        if self.datos.get('trekking_poles', 0) > 0:
            contenido += f"<li>{self.datos['trekking_poles']} Pair of Trekking poles</li>"

        contenido += """
        </ul>

        <p class="block header">WHAT TO PACK:</p>
        <ul style="margin-left: 40px; color: #333;">
            <li><strong>Documents:</strong> Original passport, student ID (if applicable).</li>
            <li><strong>Essentials:</strong> Small backpack, 1.5L water, rain poncho, sunscreen, insect repellent, personal medications, first aid kit.</li>
            <li><strong>Clothing:</strong> Hiking shirt, hiking pants, nice shirt/pants for Machu Picchu photos, 2 sets undergarments/socks, waterproof jacket, optional bathing suit (hot springs).</li>
            <li><strong>Accessories:</strong> Lightweight hiking boots, sun hat/cap, sunglasses, trekking poles (optional).</li>
            <li><strong>Extras:</strong> Camera, snacks (nuts, energy bars), extra money for souvenirs/tips.</li>
            <li><strong>Note:</strong> Pack light; no porters provided.</li>
        </ul>

        <p class="block header">ITINERARY SUMMARY:</p>
        <p style="text-align: center;"><a href="https://www.machupicchureservations.org/tour/inca-trail-2-days#itinerary" target="_blank" style="text-decoration: none; color: #FFA500; font-weight: bold; padding: 8px 16px; border: 2px solid #FFA500; border-radius: 5px;">FULL ITINERARY</a></p>
        
        <ul style="margin-left: 40px; color: #333;">
            <li><strong>Day 01 - Cusco to Machu Picchu & Aguas Calientes:</strong><br>
                  • <span style="color: #FF69B4;">Start:</span> Pick-up 3:45-4:15 AM from Cusco hotel; 1 hr 45 min drive to Ollantaytambo<br>
                  • <span style="color: #FF69B4;">Travel:</span> Train from Ollantaytambo to KM 104 (~6:40 AM)<br>
                  • <span style="color: #FF69B4;">Hike:</span> 3-hr climb (2,000-2,700 m) to Wiñaywayna; 2-hr flat hike to Sun Gate; 45-min descent to Machu Picchu<br>
                  • <span style="color: #FF69B4;">Activities:</span> Explore upper Machu Picchu (1 hr); bus to Aguas Calientes (30 min)<br>
                  • <span style="color: #FF69B4;">Stay:</span> Hotel in Aguas Calientes<br>
                  • <span style="color: #FF69B4;">Meals:</span> Lunch (packed), Dinner (7:00 PM)<br>
                  • <span style="color: #FF69B4;">Distance:</span> 12 km / 7 miles<br>
                  • <span style="color: #FF69B4;">Weather:</span> Hot, humid
            </li>
            <li><strong>Day 02 - Machu Picchu Tour & Return:</strong><br>
                  • <span style="color: #FF69B4;">Start:</span> Wake 4:30 AM; breakfast 5:00 AM; bus to Machu Picchu (5:30 AM, 30 min)<br>
                  • <span style="color: #FF69B4;">Activities:</span> 2.5-hr guided tour (lower area); 30-min free time; optional Waynapicchu/Machu Picchu Mountain (pre-booked)<br>
                  • <span style="color: #FF69B4;">Return:</span> Bus to Aguas Calientes (30 min); train to Ollantaytambo (2:30/2:55 PM, 1.5 hrs); car to Cusco (2 hrs, ~6:30 PM)<br>
                  • <span style="color: #FF69B4;">Meals:</span> Breakfast<br>
                  • <span style="color: #FF69B4;">Note:</span> Max 3 hrs at Machu Picchu; train times may vary.
            </li>
        </ul>
        """

        if self.datos['balance'] > 0:
            contenido += f"""
            <p class="block header">PAYMENT DETAILS:</p>
            <p style="color: #333;">Outstanding Balance: ${self.datos['balance']}. Pay online via WeTravel (2.9% fee) or in-person at our Cusco office (cash: no fee; card: 3.9% fee) before the briefing.</p>
            <p style="font-weight: bold; color: #32CD32;">IMPORTANT: Pay up to one day before the briefing.</p>
            """

        contenido += f"""
        <p class="block header">OFFICE ADDRESS:</p>
        <p style="font-family: Verdana, sans-serif; color: #333;">Portal Nuevo 270 Plaza Regocijo - Machu Picchu Reservations: <br> 
        <a href="https://maps.app.goo.gl/XcfipVKjbuLeY3no9" style="color: #20B2AA; font-weight: bold;">👉(Google Maps)👈</a></p>

        <div style="border-left: 4px solid #E6E6FA; padding-left: 15px; margin-top: 20px;">
            <p class="block important">IMPORTANT:</p>
            <p style="color: #333;">Please reply to this email with passport photos and your entry date into Peru.</p>
        </div>

        <p class="block header">DETAILS YOU SHOULD KNOW:</p>
        <ul style="margin-left: 40px; color: #333;">
            <li>Train times may vary by ±30 min; confirm at briefing.</li>
            <li>Carry your packed lunch on Day 1 (no cooking on trail).</li>
        </ul>

        <p style="color: #333; margin-top: 20px;">If you have any questions or need assistance, please contact <a href="https://wa.me/51908851429" 
        style="color: #20B2AA; font-weight: bold;">👉MPR👈</a>. Contact for additional info or options.</p>

        <div style="color: #333; font-size: 12px; margin-top: 20px;">
            <h2 style="color: #FFA500; font-size: 16px;">MACHUPICCHU RESERVATIONS</h2>
            <p><strong>Schedule:</strong> 7:00-22:00 hrs, Mon-Sat<br><strong>WhatsApp:</strong> <a href="https://api.whatsapp.com/send/?phone=51908851429" style="color: #20B2AA; font-weight: bold;">👉MPR👈</a></p>
        </div>
        """

        self.mostrar_confirmacion_en_html(contenido)

    def mostrar_confirmacion_en_html(self, contenido):
        nombre_archivo = "confirmacion.html"
        with open(nombre_archivo, "w", encoding="utf-8") as file:
            file.write(f"""
            <html>
            <head>
                <title>Confirmación de Reserva</title>
                <style>
                    body {{ font-family: 'Verdana', sans-serif; margin: 20px; color: #333; }}
                    p {{ line-height: 1.6; font-size: 14px; }}
                    ul {{ list-style-type: none; padding-left: 0; }}
                    ul li::before {{ content: "•"; color: #FF69B4; font-weight: bold; display: inline-block; width: 1em; margin-left: -1em; }}
                    .important {{ font-weight: bold; color: #20B2AA; }}
                    .header {{ font-size: 16px; font-weight: bold; color: #FFA500; }}
                </style>
            </head>
            <body>
                {contenido}
            </body>
            </html>
            """)
        print(f"Confirmación guardada como {nombre_archivo}")

class IncaTrail1D:
    def __init__(self, datos):
        self.datos = datos

    def generar_confirmacion(self):
        tour = 'INCA TRAIL TO MACHU PICCHU IN ONE DAY'
        tour_dias = 0
        briefing_hora = "6:00 pm"
        primer_nombre = self.datos['nombres'][0].split()[0].capitalize()

        contenido = f"""
        <p style="color: #333;">Dear {primer_nombre},</p>
        <p style="color: #333;">Your reservation is confirmed - <span style="color: #9932CC; font-weight: bold;">{tour}</span></p>
        
        <table>
            <tr>
                <td style="font-weight: bold; color: #9932CC;">START DATE:</td>
                <td style="color: #333;">{fecha_nombre(self.datos['fecha'][0], self.datos['fecha'][1], self.datos['fecha'][2])}</td>
            </tr>
            <tr>
                <td style="font-weight: bold; color: #00CED1;">BRIEFING DATE:</td>
                <td style="color: #333;">{fecha_nombre(self.datos['fecha'][0], self.datos['fecha'][1], self.datos['fecha'][2], -1)}, at {briefing_hora} at Machu Picchu Reservations.</td>
            </tr>
            <tr>
                <td style="font-weight: bold; color: #9932CC;">N° PERSON:</td>
                <td style="color: #333;">{len(self.datos['nombres']):02}</td>
            </tr>
        </table>

        <ul style="margin-left: 40px; color: #333;">
            {''.join([f"<li>{i+1}. {nombre.strip().upper()}</li>" for i, nombre in enumerate(self.datos['nombres'])])}
        </ul>

        <p class="block header">TOUR INCLUSIONS:</p>
        <ul style="margin-left: 40px;">
            <li>TRANSFER Cusco - Ollantaytambo</li>
            <li>TRAIN FROM- Ollantaytambo - KM 104</li>
            <li>01 lunch</li>
            <li>01 dinner</li>
            <li>Bus from Machu Picchu to Aguas Calientes</li>
        """

        if self.datos['machu_picchu_code'] == "0":
            contenido += "<li style='color: #FF4500;'>NOT INCLUDED: Entrance for MACHU PICCHU</li>"
        else:
            contenido += f"<li>Entrance for the INCA TRAIL + MACHU PICCHU</li>"
            contenido += f"<li>MACHU PICCHU CODES: {self.datos['machu_picchu_code']}</li>"

        if self.datos.get('montaña', '0') != '0':
            contenido += f"<li>Entrance for {self.datos['montaña']}</li>"

        if self.datos.get("vistadome_retorno", False):
            contenido += "<li>Train from Aguas Calientes to Ollantaytambo - BY TRAIN VISTADOME</li>"
        else:
            contenido += "<li>Train from Aguas Calientes to Ollantaytambo - BY TRAIN</li>"

        contenido += """
            <li>Transfer from Ollantaytambo to Cusco</li>
            <li>Tour guide</li>
        </ul>

        <p class="block header">WHAT TO PACK:</p>
        <ul style="margin-left: 40px; color: #333;">
            <li><strong>Documents:</strong> Original passport, student ID (if applicable).</li>
            <li><strong>Essentials:</strong> Small backpack, 1.5L water, sunscreen, insect repellent, personal medications.</li>
            <li><strong>Clothing:</strong> Hiking shoes, hiking socks, lightweight hiking shirt/pants, rain poncho/jacket, warm layer (e.g., jacket).</li>
            <li><strong>Accessories:</strong> Cap/hat, sunglasses, camera.</li>
            <li><strong>Note:</strong> Pack light; max 7kg including personal items (porters provided).</li>
        </ul>

        <p class="block header">ITINERARY SUMMARY:</p>
        <p style="text-align: center;"><a href="https://www.machupicchureservations.org/tour/inca-trail-to-machu-picchu-in-one-day#itinerary" target="_blank" style="text-decoration: none; color: #9932CC; font-weight: bold; padding: 8px 16px; border: 2px solid #9932CC; border-radius: 5px;">FULL ITINERARY</a></p>
        
        <ul style="margin-left: 40px; color: #333;">
            <li><strong>Day 01 - Cusco to Machu Picchu & Return:</strong><br>
                  • <span style="color: #FF4500;">Start:</span> Pick-up 4:00 AM from Cusco hotel; 1 hr 45 min drive to Ollantaytambo<br>
                  • <span style="color: #FF4500;">Travel:</span> Train to KM 104 (6:10/6:40 AM); checkpoint at KM 104<br>
                  • <span style="color: #FF4500;">Hike:</span> 3-3.5 hr uphill to Wiñaywayna (2,000-2,720 m); 2 hr to Sun Gate; descent to Machu Picchu<br>
                  • <span style="color: #FF4500;">Activities:</span> Short guided tour (~1 hr), photos; bus to Aguas Calientes (5:00 PM, 30 min)<br>
                  • <span style="color: #FF4500;">Return:</span> Dinner in Aguas Calientes; train to Ollantaytambo (6:30 PM, 1.5 hrs); car to Cusco (~10:00 PM)<br>
                  • <span style="color: #FF4500;">Distance:</span> 15 km / 8 miles<br>
                  • <span style="color: #FF4500;">Meals:</span> Lunch (packed), Dinner<br>
                  • <span style="color: #FF4500;">Weather:</span> Hot, humid
            </li>
        </ul>
        """

        if self.datos['balance'] > 0:
            contenido += f"""
            <p class="block header">PAYMENT DETAILS:</p>
            <p style="color: #333;">Outstanding Balance: ${self.datos['balance']}. Pay online via WeTravel (2.9% fee) or in-person at our Cusco office (cash: no fee; card: 3.9% fee) before the briefing.</p>
            <p style="font-weight: bold; color: #FF69B4;">IMPORTANT: Pay up to one day before the briefing.</p>
            """

        contenido += f"""
        <p class="block header">OFFICE ADDRESS:</p>
        <p style="font-family: Verdana, sans-serif; color: #333;">Portal Nuevo 270 Plaza Regocijo - Machu Picchu Reservations: <br> 
        <a href="https://maps.app.goo.gl/XcfipVKjbuLeY3no9" style="color: #00CED1; font-weight: bold;">👉(Google Maps)👈</a></p>

        <div style="border-left: 4px solid #F0E68C; padding-left: 15px; margin-top: 20px;">
            <p class="block important">IMPORTANT:</p>
            <p style="color: #333;">Please reply to this email with passport photos and your entry date into Peru.</p>
        </div>

        <p class="block header">DETAILS YOU SHOULD KNOW:</p>
        <ul style="margin-left: 40px; color: #333;">
            <li>Carry packed lunch provided at KM 104 (no cooking on trail).</li>
            <li>Train times may vary; confirm at briefing.</li>
            <li>No mountain hikes possible due to time constraints.</li>
        </ul>

        <p style="color: #333; margin-top: 20px;">If you have any questions or need assistance, please contact <a href="https://wa.me/51908851429" 
        style="color: #00CED1; font-weight: bold;">👉MPR👈</a>. Contact for additional info or options.</p>

        <div style="color: #333; font-size: 12px; margin-top: 20px;">
            <h2 style="color: #9932CC; font-size: 16px;">MACHUPICCHU RESERVATIONS</h2>
            <p><strong>Schedule:</strong> 7:00-22:00 hrs, Mon-Sat<br><strong>WhatsApp:</strong> <a href="https://api.whatsapp.com/send/?phone=51908851429" style="color: #00CED1; font-weight: bold;">👉MPR👈</a></p>
        </div>
        """

        self.mostrar_confirmacion_en_html(contenido)

    def mostrar_confirmacion_en_html(self, contenido):
        nombre_archivo = "confirmacion.html"
        with open(nombre_archivo, "w", encoding="utf-8") as file:
            file.write(f"""
            <html>
            <head>
                <title>Confirmación de Reserva</title>
                <style>
                    body {{ font-family: 'Verdana', sans-serif; margin: 20px; color: #333; }}
                    p {{ line-height: 1.6; font-size: 14px; }}
                    ul {{ list-style-type: none; padding-left: 0; }}
                    ul li::before {{ content: "•"; color: #FF4500; font-weight: bold; display: inline-block; width: 1em; margin-left: -1em; }}
                    .important {{ font-weight: bold; color: #00CED1; }}
                    .header {{ font-size: 16px; font-weight: bold; color: #9932CC; }}
                </style>
            </head>
            <body>
                {contenido}
            </body>
            </html>
            """)
        print(f"Confirmación guardada como {nombre_archivo}")

class IncaJungle4DTrain:
    def __init__(self, datos):
        self.datos = datos
        self.vistadome_ida = datos.get("vistadome_ida", False)
        self.vistadome_retorno = datos.get("vistadome_retorno", False)

    def generar_confirmacion(self):
        tour = 'INCA JUNGLE TRAIL TO MACHU PICCHU 4D-3N'
        tour_dias = 3
        briefing_hora = "18:00"
        primer_nombre = self.datos['nombres'][0].split()[0].capitalize()

        contenido = (
            f"<p style='color: #333;'>Dear {primer_nombre},</p>"
            f"<p style='color: #333;'>Your reservation is confirmed - <span style='color: #FF1493; font-weight: bold;'>{tour}</span></p>"
            f"<table>"
            f"<tr><td style='font-weight: bold; color: #FF1493;'>START DATE:</td><td style='color: #333;'>{fecha_nombre(self.datos['fecha'][0], self.datos['fecha'][1], self.datos['fecha'][2])}</td></tr>"
            f"<tr><td style='font-weight: bold; color: #FF1493;'>RETURN DATE:</td><td style='color: #333;'>{fecha_nombre(self.datos['fecha'][0], self.datos['fecha'][1], self.datos['fecha'][2], tour_dias)}</td></tr>"
            f"<tr><td style='font-weight: bold; color: #40E0D0;'>BRIEFING DATE:</td><td style='color: #333;'>{fecha_nombre(self.datos['fecha'][0], self.datos['fecha'][1], self.datos['fecha'][2], -1)}, at {briefing_hora} at Machu Picchu Reservations.</td></tr>"
            f"<tr><td style='font-weight: bold; color: #FF1493;'>N° PERSON:</td><td style='color: #333;'>{len(self.datos['nombres']):02}</td></tr>"
            f"</table>"
            f"<ul style='margin-left: 40px; color: #333;'>"
            + ''.join([f"<li>{i+1}. {nombre.strip().upper()}</li>" for i, nombre in enumerate(self.datos['nombres'])])
            + "</ul>"
        )

        contenido += "<p class='block header'>TOUR INCLUSIONS:</p><ul style='margin-left: 40px;'>"
        contenido += "<li>Transportation to the trailhead</li>"
        contenido += "<li>3 breakfasts</li>"
        contenido += "<li>3 lunches</li>"
        contenido += "<li>3 dinners</li>"
        contenido += "<li>3-night hostel</li>"

        if self.datos['machu_picchu_code'] == "0":
            contenido += "<li style='color: #FF4500;'>NOT INCLUDED: Entrance for MACHU PICCHU</li>"
        else:
            contenido += f"<li>Entrance for MACHU PICCHU</li>"
            contenido += f"<li>MACHU PICCHU CODES: {self.datos['machu_picchu_code']}</li>"

        if self.datos.get('montaña', '0') != '0':
            contenido += f"<li>Entrance for {self.datos['montaña']}</li>"

        if self.vistadome_retorno:
            contenido += "<li>Train from Aguas Calientes to Ollantaytambo - BY TRAIN VISTADOME</li>"
        else:
            contenido += "<li>Train from Aguas Calientes to Ollantaytambo - BY TRAIN</li>"

        contenido += (
            "<li>Transfer from Ollantaytambo to Cusco</li>"
            "<li>Guide</li>"
            "<li>Biking</li>"
            "<li>Rafting</li>"
            "<li>Zipline</li>"
            "</ul>"
        )

        contenido += f"""
        <p class='block header'>WHAT TO PACK:</p>
        <ul style='margin-left: 40px; color: #333;'>
            <li><strong>Essentials:</strong> Passport, student ID (if applicable), 25-30L backpack.</li>
            <li><strong>Clothing:</strong> Wool hat/beanie, sun hat, gloves, 2-3 long-sleeve t-shirts, sweater/fleece, 2 pairs pants/leggings, hiking shoes, 1-2 pairs wool socks, rain gear (jacket/pants/poncho), sandals/flip-flops, bath linen/towel.</li>
            <li><strong>Toiletries/Health:</strong> Toothbrush, toothpaste, sunscreen, insect repellent, personal medications.</li>
            <li><strong>Extras:</strong> Snacks (chocolate, nuts, etc.), extra cash in Soles.</li>
            <li><strong>Note:</strong> Pack light; no luggage transfer, but backpacks can be secured during activities.</li>
        </ul>

        <p class='block header'>ITINERARY SUMMARY:</p>
        <p style='text-align: center;'><a href='https://www.machupicchureservations.org/tour/inca-jungle-trail-4-days#itinerary' target='_blank' style='text-decoration: none; color: #FF1493; font-weight: bold; padding: 8px 16px; border: 2px solid #FF1493; border-radius: 5px;'>FULL ITINERARY</a></p>
        
        <ul style='margin-left: 40px; color: #333;'>
            <li><strong>Day 01 - Cusco to Santa Maria:</strong><br>
                  • <span style='color: #00FF7F;'>Start:</span> Pick-up 6:00 AM from Cusco hotel; 2-hr drive to Ollantaytambo (breakfast)<br>
                  • <span style='color: #00FF7F;'>Travel:</span> Drive to Abra Malaga (4,350 m)<br>
                  • <span style='color: #00FF7F;'>Activities:</span> 65 km / 3-4 hr downhill biking to Santa Maria (1,430 m); visit Huamanmarca; 1-1.5 hr rafting<br>
                  • <span style='color: #00FF7F;'>Stay:</span> Hotel in Santa Maria<br>
                  • <span style='color: #00FF7F;'>Meals:</span> Breakfast, Lunch, Dinner<br>
                  • <span style='color: #00FF7F;'>Difficulty:</span> Moderate<br>
                  • <span style='color: #00FF7F;'>Weather:</span> Warm, windy
            </li>
            <li><strong>Day 02 - Santa Maria to Santa Teresa:</strong><br>
                  • <span style='color: #00FF7F;'>Start:</span> Breakfast 6:00 AM<br>
                  • <span style='color: #00FF7F;'>Hike:</span> 22 km / 7-8 hrs; 45-min car route, 3-hr Inca Trail, 3.5-hr Vilcanota River trek<br>
                  • <span style='color: #00FF7F;'>Activities:</span> Lunch in Quellomayo; 2 hrs at Colcamayo hot springs<br>
                  • <span style='color: #00FF7F;'>Stay:</span> Hotel in Santa Teresa<br>
                  • <span style='color: #00FF7F;'>Meals:</span> Breakfast, Lunch, Dinner<br>
                  • <span style='color: #00FF7F;'>Difficulty:</span> Moderate<br>
                  • <span style='color: #00FF7F;'>Weather:</span> Warm, tropical
            </li>
            <li><strong>Day 03 - Santa Teresa to Aguas Calientes:</strong><br>
                  • <span style='color: #00FF7F;'>Start:</span> Breakfast 6:30 AM; pick-up 8:00 AM<br>
                  • <span style='color: #00FF7F;'>Activities:</span> 2-hr ziplining (4 lines, suspension bridge); 1-hr car ride to Hidroelectrica (lunch)<br>
                  • <span style='color: #00FF7F;'>Hike:</span> 11 km / 3-3.5 hrs along train tracks to Aguas Calientes<br>
                  • <span style='color: #00FF7F;'>Stay:</span> Hotel in Aguas Calientes<br>
                  • <span style='color: #00FF7F;'>Meals:</span> Breakfast, Lunch, Dinner (7:00 PM)<br>
                  • <span style='color: #00FF7F;'>Difficulty:</span> Moderate<br>
                  • <span style='color: #00FF7F;'>Weather:</span> Warm, tropical
            </li>
            <li><strong>Day 04 - Machu Picchu & Train Return:</strong><br>
                  • <span style='color: #00FF7F;'>Start:</span> Wake 4:00 AM; breakfast; hike (1.5 hrs) or bus ($12, 30 min) to Machu Picchu (5:30 AM)<br>
                  • <span style='color: #00FF7F;'>Activities:</span> 2.5-hr guided tour (Circuit 01/02 preferred); optional Huayna Picchu/Machu Picchu Mountain ($60, pre-booked)<br>
                  • <span style='color: #00FF7F;'>Return:</span> Bus to Aguas Calientes; train to Ollantaytambo (2:30/2:55 PM, 1.5 hrs); car to Cusco (~6:30 PM)<br>
                  • <span style='color: #00FF7F;'>Meals:</span> Breakfast<br>
            </li>
        </ul>
        """

        if self.datos['balance'] > 0:
            contenido += f"""
            <p class='block header'>PAYMENT DETAILS:</p>
            <p style='color: #333;'>Outstanding Balance: ${self.datos['balance']}. Pay online via WeTravel (2.9% fee) or in-person at our Cusco office (cash: no fee; card: 3.9% fee) before the briefing.</p>
            <p style='font-weight: bold; color: #FFD700;'>IMPORTANT: Pay up to one day before the briefing.</p>
            """

        contenido += f"""
        <p class='block header'>OFFICE ADDRESS:</p>
        <p style='font-family: Verdana, sans-serif; color: #333;'>Portal Nuevo 270 Plaza Regocijo - Machu Picchu Reservations: <br> 
        <a href='https://maps.app.goo.gl/XcfipVKjbuLeY3no9' style='color: #40E0D0; font-weight: bold;'>👉(Google Maps)👈</a></p>

        <div style='border-left: 4px solid #FFA07A; padding-left: 15px; margin-top: 20px;'>
            <p class='block important'>IMPORTANT:</p>
            <p style='color: #333;'>Please reply to this email with passport photos and your entry date into Peru.</p>
        </div>

        <p class='block header'>DETAILS YOU SHOULD KNOW:</p>
        <ul style='margin-left: 40px; color: #333;'>
            <li>Bus tickets to Machu Picchu ($12) not included; arrange night before or morning of.</li>
        </ul>

        <p style='color: #333; margin-top: 20px;'>If you have any questions or need assistance, please contact <a href='https://wa.me/51908851429' 
        style='color: #40E0D0; font-weight: bold;'>👉MPR👈</a>. Contact for additional info or options.</p>

        <div style='color: #333; font-size: 12px; margin-top: 20px;'>
            <h2 style='color: #FF1493; font-size: 16px;'>MACHUPICCHU RESERVATIONS</h2>
            <p><strong>Schedule:</strong> 7:00-22:00 hrs, Mon-Sat<br><strong>WhatsApp:</strong> <a href='https://api.whatsapp.com/send/?phone=51908851429' style='color: #40E0D0; font-weight: bold;'>👉MPR👈</a></p>
        </div>
        """

        self.mostrar_confirmacion_en_html(contenido)

    def mostrar_confirmacion_en_html(self, contenido):
        nombre_archivo = "confirmacion.html"
        with open(nombre_archivo, "w", encoding="utf-8") as file:
            file.write(f"""
            <html>
            <head>
                <title>Confirmación de Reserva</title>
                <style>
                    body {{ font-family: 'Verdana', sans-serif; margin: 20px; color: #333; }}
                    p {{ line-height: 1.6; font-size: 14px; }}
                    ul {{ list-style-type: none; padding-left: 0; }}
                    ul li::before {{ content: "•"; color: #00FF7F; font-weight: bold; display: inline-block; width: 1em; margin-left: -1em; }}
                    .important {{ font-weight: bold; color: #40E0D0; }}
                    .header {{ font-size: 16px; font-weight: bold; color: #FF1493; }}
                </style>
            </head>
            <body>
                {contenido}
            </body>
            </html>
            """)
        print(f"Confirmación guardada como {nombre_archivo}")

class IncaJungle4DCar:
    def __init__(self, datos):
        self.datos = datos

    def generar_confirmacion(self):
        tour = 'INCA JUNGLE TRAIL TO MACHU PICCHU 4D-3N'
        tour_dias = 3
        briefing_hora = "18:00"
        primer_nombre = self.datos['nombres'][0].split()[0].capitalize()

        contenido = f"""
        <p style='color: #333;'>Dear {primer_nombre},</p>
        <p style='color: #333;'>Your reservation is confirmed - <span style='color: #FF1493; font-weight: bold;'>{tour}</span></p>
        
        <table>
            <tr>
                <td style='font-weight: bold; color: #FF1493;'>START DATE:</td>
                <td style='color: #333;'>{fecha_nombre(self.datos['fecha'][0], self.datos['fecha'][1], self.datos['fecha'][2])}</td>
            </tr>
            <tr>
                <td style='font-weight: bold; color: #FF1493;'>RETURN DATE:</td>
                <td style='color: #333;'>{fecha_nombre(self.datos['fecha'][0], self.datos['fecha'][1], self.datos['fecha'][2], tour_dias)}</td>
            </tr>
            <tr>
                <td style='font-weight: bold; color: #40E0D0;'>BRIEFING DATE:</td>
                <td style='color: #333;'>{fecha_nombre(self.datos['fecha'][0], self.datos['fecha'][1], self.datos['fecha'][2], -1)}, at {briefing_hora} at Machu Picchu Reservations.</td>
            </tr>
            <tr>
                <td style='font-weight: bold; color: #FF1493;'>N° PERSON:</td>
                <td style='color: #333;'>{len(self.datos['nombres']):02}</td>
            </tr>
        </table>

        <ul style='margin-left: 40px; color: #333;'>
            {''.join([f"<li>{i+1}. {nombre.strip().upper()}</li>" for i, nombre in enumerate(self.datos['nombres'])])}
        </ul>

        <p class='block header'>TOUR INCLUSIONS:</p>
        <ul style='margin-left: 40px;'>
            <li>Transportation to the trailhead</li>
            <li>3 breakfasts</li>
            <li>3 lunches</li>
            <li>3 dinners</li>
            <li>3-night hostel</li>
        """

        if self.datos['machu_picchu_code'] == "0":
            contenido += "<li style='color: #FF4500;'>NOT INCLUDED: Entrance for MACHU PICCHU</li>"
        else:
            contenido += f"<li>Entrance for MACHU PICCHU</li>"
            contenido += f"<li>MACHU PICCHU CODES: {self.datos['machu_picchu_code']}</li>"

        contenido += """
            <li>Transportation from Hidroeléctrica to Cusco - BY CAR</li>
            <li>Guide</li>
            <li>Biking</li>
            <li>Rafting</li>
            <li>Zipline</li>
        </ul>

        <p class='block header'>WHAT TO PACK:</p>
        <ul style='margin-left: 40px; color: #333;'>
            <li><strong>Essentials:</strong> Passport, student ID (if applicable), 25-30L backpack.</li>
            <li><strong>Clothing:</strong> Wool hat/beanie, sun hat, gloves, 2-3 long-sleeve t-shirts, sweater/fleece, 2 pairs pants/leggings, hiking shoes, 1-2 pairs wool socks, rain gear (jacket/pants/poncho), sandals/flip-flops, bath linen/towel.</li>
            <li><strong>Toiletries/Health:</strong> Toothbrush, toothpaste, sunscreen, insect repellent, personal medications.</li>
            <li><strong>Extras:</strong> Snacks (chocolate, nuts, etc.), extra cash in Soles.</li>
            <li><strong>Note:</strong> Pack light; no luggage transfer, but backpacks can be secured during activities.</li>
        </ul>

        <p class='block header'>ITINERARY SUMMARY:</p>
        <p style='text-align: center;'><a href='https://www.machupicchureservations.org/tour/inca-jungle-trail-4-days#itinerary' target='_blank' style='text-decoration: none; color: #FF1493; font-weight: bold; padding: 8px 16px; border: 2px solid #FF1493; border-radius: 5px;'>FULL ITINERARY</a></p>
        
        <ul style='margin-left: 40px; color: #333;'>
            <li><strong>Day 01 - Cusco to Santa Maria:</strong><br>
                  • <span style='color: #00FF7F;'>Start:</span> Pick-up 6:00 AM from Cusco hotel; 2-hr drive to Ollantaytambo (breakfast)<br>
                  • <span style='color: #00FF7F;'>Travel:</span> Drive to Abra Malaga (4,350 m)<br>
                  • <span style='color: #00FF7F;'>Activities:</span> 65 km / 3-4 hr downhill biking to Santa Maria (1,430 m); visit Huamanmarca; 1-1.5 hr rafting<br>
                  • <span style='color: #00FF7F;'>Stay:</span> Hotel in Santa Maria<br>
                  • <span style='color: #00FF7F;'>Meals:</span> Breakfast, Lunch, Dinner<br>
                  • <span style='color: #00FF7F;'>Difficulty:</span> Moderate<br>
                  • <span style='color: #00FF7F;'>Weather:</span> Warm, windy
            </li>
            <li><strong>Day 02 - Santa Maria to Santa Teresa:</strong><br>
                  • <span style='color: #00FF7F;'>Start:</span> Breakfast 6:00 AM<br>
                  • <span style='color: #00FF7F;'>Hike:</span> 22 km / 7-8 hrs; 45-min car route, 3-hr Inca Trail, 3.5-hr Vilcanota River trek<br>
                  • <span style='color: #00FF7F;'>Activities:</span> Lunch in Quellomayo; 2 hrs at Colcamayo hot springs<br>
                  • <span style='color: #00FF7F;'>Stay:</span> Hotel in Santa Teresa<br>
                  • <span style='color: #00FF7F;'>Meals:</span> Breakfast, Lunch, Dinner<br>
                  • <span style='color: #00FF7F;'>Difficulty:</span> Moderate<br>
                  • <span style='color: #00FF7F;'>Weather:</span> Warm, tropical
            </li>
            <li><strong>Day 03 - Santa Teresa to Aguas Calientes:</strong><br>
                  • <span style='color: #00FF7F;'>Start:</span> Breakfast 6:30 AM; pick-up 8:00 AM<br>
                  • <span style='color: #00FF7F;'>Activities:</span> 2-hr ziplining (4 lines, suspension bridge); 1-hr car ride to Hidroelectrica (lunch)<br>
                  • <span style='color: #00FF7F;'>Hike:</span> 11 km / 3-3.5 hrs along train tracks to Aguas Calientes<br>
                  • <span style='color: #00FF7F;'>Stay:</span> Hotel in Aguas Calientes<br>
                  • <span style='color: #00FF7F;'>Meals:</span> Breakfast, Lunch, Dinner (7:00 PM)<br>
                  • <span style='color: #00FF7F;'>Difficulty:</span> Moderate<br>
                  • <span style='color: #00FF7F;'>Weather:</span> Warm, tropical
            </li>
            <li><strong>Day 04 - Machu Picchu & Car Return:</strong><br>
                  • <span style='color: #00FF7F;'>Start:</span> Wake 4:00 AM; breakfast; hike (1.5 hrs) or bus ($12, 30 min) to Machu Picchu (5:30 AM)<br>
                  • <span style='color: #00FF7F;'>Activities:</span> 2.5-hr guided tour (Circuit 01/02 preferred)<br>
                  • <span style='color: #00FF7F;'>Return:</span> Hike to Hidroeléctrica (3-3.5 hrs, leave 10:30 AM); car to Cusco (2:30 PM, 6 hrs, ~9:30 PM)<br>
                  • <span style='color: #00FF7F;'>Meals:</span> Breakfast<br>
            </li>
        </ul>
        """

        if self.datos['balance'] > 0:
            contenido += f"""
            <p class='block header'>PAYMENT DETAILS:</p>
            <p style='color: #333;'>Outstanding Balance: ${self.datos['balance']}. Pay online via WeTravel (2.9% fee) or in-person at our Cusco office (cash: no fee; card: 3.9% fee) before the briefing.</p>
            <p style='font-weight: bold; color: #FFD700;'>IMPORTANT: Pay up to one day before the briefing.</p>
            """

        contenido += f"""
        <p class='block header'>OFFICE ADDRESS:</p>
        <p style='font-family: Verdana, sans-serif; color: #333;'>Portal Nuevo 270 Plaza Regocijo - Machu Picchu Reservations: <br> 
        <a href='https://maps.app.goo.gl/XcfipVKjbuLeY3no9' style='color: #40E0D0; font-weight: bold;'>👉(Google Maps)👈</a></p>

        <div style='border-left: 4px solid #FFA07A; padding-left: 15px; margin-top: 20px;'>
            <p class='block important'>IMPORTANT:</p>
            <p style='color: #333;'>Please reply to this email with passport photos and your entry date into Peru.</p>
        </div>

        <p class='block header'>DETAILS YOU SHOULD KNOW:</p>
        <ul style='margin-left: 40px; color: #333;'>
            <li>Bus tickets to Machu Picchu ($12) not included; arrange night before or morning of.</li>
        </ul>

        <p style='color: #333; margin-top: 20px;'>If you have any questions or need assistance, please contact <a href='https://wa.me/51908851429' 
        style='color: #40E0D0; font-weight: bold;'>👉MPR👈</a>. Contact for additional info or options.</p>

        <div style='color: #333; font-size: 12px; margin-top: 20px;'>
            <h2 style='color: #FF1493; font-size: 16px;'>MACHUPICCHU RESERVATIONS</h2>
            <p><strong>Schedule:</strong> 7:00-22:00 hrs, Mon-Sat<br><strong>WhatsApp:</strong> <a href='https://api.whatsapp.com/send/?phone=51908851429' style='color: #40E0D0; font-weight: bold;'>👉MPR👈</a></p>
        </div>
        """

        self.mostrar_confirmacion_en_html(contenido)

    def mostrar_confirmacion_en_html(self, contenido):
        nombre_archivo = "confirmacion.html"
        with open(nombre_archivo, "w", encoding="utf-8") as file:
            file.write(f"""
            <html>
            <head>
                <title>Confirmación de Reserva</title>
                <style>
                    body {{ font-family: 'Verdana', sans-serif; margin: 20px; color: #333; }}
                    p {{ line-height: 1.6; font-size: 14px; }}
                    ul {{ list-style-type: none; padding-left: 0; }}
                    ul li::before {{ content: "•"; color: #00FF7F; font-weight: bold; display: inline-block; width: 1em; margin-left: -1em; }}
                    .important {{ font-weight: bold; color: #40E0D0; }}
                    .header {{ font-size: 16px; font-weight: bold; color: #FF1493; }}
                </style>
            </head>
            <body>
                {contenido}
            </body>
            </html>
            """)
        print(f"Confirmación guardada como {nombre_archivo}")

class IncaJungle3DTrain:
    def __init__(self, datos):
        self.datos = datos

    def generar_confirmacion(self):
        tour = 'INCA JUNGLE TRAIL TO MACHU PICCHU 3D-2N'
        tour_dias = 2
        briefing_hora = "6:00 pm"
        primer_nombre = self.datos['nombres'][0].split()[0].capitalize()

        contenido = f"""
        <p style='color: #333;'>Dear {primer_nombre},</p>
        <p style='color: #333;'>Your reservation is confirmed - <span style='color: #87CEFA; font-weight: bold;'>{tour}</span></p>
        
        <table>
            <tr>
                <td style='font-weight: bold; color: #87CEFA;'>START DATE:</td>
                <td style='color: #333;'>{fecha_nombre(self.datos['fecha'][0], self.datos['fecha'][1], self.datos['fecha'][2])}</td>
            </tr>
            <tr>
                <td style='font-weight: bold; color: #87CEFA;'>RETURN DATE:</td>
                <td style='color: #333;'>{fecha_nombre(self.datos['fecha'][0], self.datos['fecha'][1], self.datos['fecha'][2], tour_dias)}</td>
            </tr>
            <tr>
                <td style='font-weight: bold; color: #FF69B4;'>BRIEFING DATE:</td>
                <td style='color: #333;'>{fecha_nombre(self.datos['fecha'][0], self.datos['fecha'][1], self.datos['fecha'][2], -1)}, at {briefing_hora} at Machu Picchu Reservations.</td>
            </tr>
            <tr>
                <td style='font-weight: bold; color: #87CEFA;'>N° PERSON:</td>
                <td style='color: #333;'>{len(self.datos['nombres']):02}</td>
            </tr>
        </table>

        <ul style='margin-left: 40px; color: #333;'>
            {''.join([f"<li>{i+1}. {nombre.strip().upper()}</li>" for i, nombre in enumerate(self.datos['nombres'])])}
        </ul>

        <p class='block header'>TOUR INCLUSIONS:</p>
        <ul style='margin-left: 40px;'>
            <li>Transportation to the trailhead</li>
            <li>2 breakfasts</li>
            <li>2 lunches</li>
            <li>2 dinners</li>
            <li>2-night hostel</li>
        """

        if self.datos['machu_picchu_code'] == "0":
            contenido += "<li style='color: #FF4500;'>NOT INCLUDED: Entrance for MACHU PICCHU</li>"
        else:
            contenido += f"<li>Entrance for MACHU PICCHU</li>"
            contenido += f"<li>MACHU PICCHU CODES: {self.datos['machu_picchu_code']}</li>"

        if self.datos.get('montaña', '0') != '0':
            contenido += f"<li>Entrance for {self.datos['montaña']}</li>"

        if self.datos.get("vistadome_retorno", False):
            contenido += "<li>Train from Aguas Calientes to Ollantaytambo - BY TRAIN VISTADOME</li>"
        else:
            contenido += "<li>Train from Aguas Calientes to Ollantaytambo - BY TRAIN</li>"

        contenido += """
            <li>Transfer from Ollantaytambo to Cusco</li>
            <li>Guide</li>
            <li>Biking</li>
            <li>Rafting</li>
            <li>Zipline</li>
        </ul>

        <p class='block header'>WHAT TO PACK:</p>
        <ul style='margin-left: 40px; color: #333;'>
            <li><strong>Essentials:</strong> Passport, student ID (if applicable), 25-30L backpack.</li>
            <li><strong>Clothing:</strong> Wool hat/beanie, sun hat, gloves, 2-3 long-sleeve t-shirts, sweater/fleece, 2 pairs pants/leggings, hiking shoes, 1-2 pairs wool socks, rain gear (jacket/pants/poncho), sandals/flip-flops, bath linen/towel.</li>
            <li><strong>Toiletries/Health:</strong> Toothbrush, toothpaste, sunscreen, insect repellent, personal medications.</li>
            <li><strong>Extras:</strong> Snacks (chocolate, nuts, etc.), extra cash in Soles.</li>
            <li><strong>Note:</strong> Pack light; no luggage transfer, but backpacks can be secured during activities.</li>
        </ul>

        <p class='block header'>ITINERARY SUMMARY:</p>
        <p style='text-align: center;'><a href='https://www.machupicchureservations.org/tour/inca-jungle-trail-3-days#itinerary' target='_blank' style='text-decoration: none; color: #87CEFA; font-weight: bold; padding: 8px 16px; border: 2px solid #87CEFA; border-radius: 5px;'>FULL ITINERARY</a></p>
        
        <ul style='margin-left: 40px; color: #333;'>
            <li><strong>Day 01 - Cusco to Santa Teresa:</strong><br>
                  • <span style='color: #FFB6C1;'>Start:</span> Pick-up 6:00 AM from Cusco hotel; 2-hr drive to Ollantaytambo (breakfast)<br>
                  • <span style='color: #FFB6C1;'>Travel:</span> Drive to Abra Malaga (4,350 m)<br>
                  • <span style='color: #FFB6C1;'>Activities:</span> 65 km / 3-4 hr downhill biking to Santa Maria (1,430 m); visit Huamanmarca; 1-1.5 hr rafting; 1-hr car to Santa Teresa<br>
                  • <span style='color: #FFB6C1;'>Stay:</span> Hotel in Santa Teresa<br>
                  • <span style='color: #FFB6C1;'>Meals:</span> Breakfast, Lunch, Dinner<br>
                  • <span style='color: #FFB6C1;'>Difficulty:</span> Moderate<br>
                  • <span style='color: #FFB6C1;'>Weather:</span> Warm, windy
            </li>
            <li><strong>Day 02 - Santa Teresa to Aguas Calientes:</strong><br>
                  • <span style='color: #FFB6C1;'>Start:</span> Breakfast 6:30 AM; pick-up 8:00 AM<br>
                  • <span style='color: #FFB6C1;'>Activities:</span> 2-hr ziplining (4 lines, suspension bridge); 1-hr car ride to Hidroelectrica (lunch)<br>
                  • <span style='color: #FFB6C1;'>Hike:</span> 11 km / 3-3.5 hrs along train tracks to Aguas Calientes<br>
                  • <span style='color: #FFB6C1;'>Stay:</span> Hotel in Aguas Calientes<br>
                  • <span style='color: #FFB6C1;'>Meals:</span> Breakfast, Lunch, Dinner (7:00 PM)<br>
                  • <span style='color: #FFB6C1;'>Difficulty:</span> Moderate<br>
                  • <span style='color: #FFB6C1;'>Weather:</span> Warm, tropical
            </li>
            <li><strong>Day 03 - Machu Picchu & Train Return:</strong><br>
                  • <span style='color: #FFB6C1;'>Start:</span> Wake 4:00 AM; breakfast; hike (1.5 hrs) or bus ($12, 30 min) to Machu Picchu (5:30 AM)<br>
                  • <span style='color: #FFB6C1;'>Activities:</span> 2.5-hr guided tour (Circuit 01/02 preferred); optional Huayna Picchu/Machu Picchu Mountain ($60, pre-booked)<br>
                  • <span style='color: #FFB6C1;'>Return:</span> Bus to Aguas Calientes; train to Ollantaytambo (2:30/2:55 PM, 1.5 hrs); car to Cusco (~6:30 PM)<br>
                  • <span style='color: #FFB6C1;'>Meals:</span> Breakfast<br>
            </li>
        </ul>
        """

        if self.datos['balance'] > 0:
            contenido += f"""
            <p class='block header'>PAYMENT DETAILS:</p>
            <p style='color: #333;'>Outstanding Balance: ${self.datos['balance']}. Pay online via WeTravel (2.9% fee) or in-person at our Cusco office (cash: no fee; card: 3.9% fee) before the briefing.</p>
            <p style='font-weight: bold; color: #FF4500;'>IMPORTANT: Pay up to one day before the briefing.</p>
            """

        contenido += f"""
        <p class='block header'>OFFICE ADDRESS:</p>
        <p style='font-family: Verdana, sans-serif; color: #333;'>Portal Nuevo 270 Plaza Regocijo - Machu Picchu Reservations: <br> 
        <a href='https://maps.app.goo.gl/XcfipVKjbuLeY3no9' style='color: #FF69B4; font-weight: bold;'>👉(Google Maps)👈</a></p>

        <div style='border-left: 4px solid #98FB98; padding-left: 15px; margin-top: 20px;'>
            <p class='block important'>IMPORTANT:</p>
            <p style='color: #333;'>Please reply to this email with passport photos and your entry date into Peru.</p>
        </div>

        <p class='block header'>DETAILS YOU SHOULD KNOW:</p>
        <ul style='margin-left: 40px; color: #333;'>
            <li>Bus tickets to Machu Picchu ($12) not included; arrange night before or morning of.</li>
        </ul>

        <p style='color: #333; margin-top: 20px;'>If you have any questions or need assistance, please contact <a href='https://wa.me/51908851429' 
        style='color: #FF69B4; font-weight: bold;'>👉MPR👈</a>. Contact for additional info or options.</p>

        <div style='color: #333; font-size: 12px; margin-top: 20px;'>
            <h2 style='color: #87CEFA; font-size: 16px;'>MACHUPICCHU RESERVATIONS</h2>
            <p><strong>Schedule:</strong> 7:00-22:00 hrs, Mon-Sat<br><strong>WhatsApp:</strong> <a href='https://api.whatsapp.com/send/?phone=51908851429' style='color: #FF69B4; font-weight: bold;'>👉MPR👈</a></p>
        </div>
        """

        self.mostrar_confirmacion_en_html(contenido)

    def mostrar_confirmacion_en_html(self, contenido):
        nombre_archivo = "confirmacion.html"
        with open(nombre_archivo, "w", encoding="utf-8") as file:
            file.write(f"""
            <html>
            <head>
                <title>Confirmación de Reserva</title>
                <style>
                    body {{ font-family: 'Verdana', sans-serif; margin: 20px; color: #333; }}
                    p {{ line-height: 1.6; font-size: 14px; }}
                    ul {{ list-style-type: none; padding-left: 0; }}
                    ul li::before {{ content: "•"; color: #FFB6C1; font-weight: bold; display: inline-block; width: 1em; margin-left: -1em; }}
                    .important {{ font-weight: bold; color: #FF69B4; }}
                    .header {{ font-size: 16px; font-weight: bold; color: #87CEFA; }}
                </style>
            </head>
            <body>
                {contenido}
            </body>
            </html>
            """)
        print(f"Confirmación guardada como {nombre_archivo}")

class IncaJungle3DCar:
    def __init__(self, datos):
        self.datos = datos

    def generar_confirmacion(self):
        tour = 'INCA JUNGLE TRAIL TO MACHU PICCHU 3D-2N'
        tour_dias = 2
        briefing_hora = "6:00 pm"
        primer_nombre = self.datos['nombres'][0].split()[0].capitalize()

        contenido = f"""
        <p style='color: #333;'>Dear {primer_nombre},</p>
        <p style='color: #333;'>Your reservation is confirmed - <span style='color: #87CEFA; font-weight: bold;'>{tour}</span></p>
        
        <table>
            <tr>
                <td style='font-weight: bold; color: #87CEFA;'>START DATE:</td>
                <td style='color: #333;'>{fecha_nombre(self.datos['fecha'][0], self.datos['fecha'][1], self.datos['fecha'][2])}</td>
            </tr>
            <tr>
                <td style='font-weight: bold; color: #87CEFA;'>RETURN DATE:</td>
                <td style='color: #333;'>{fecha_nombre(self.datos['fecha'][0], self.datos['fecha'][1], self.datos['fecha'][2], tour_dias)}</td>
            </tr>
            <tr>
                <td style='font-weight: bold; color: #FF69B4;'>BRIEFING DATE:</td>
                <td style='color: #333;'>{fecha_nombre(self.datos['fecha'][0], self.datos['fecha'][1], self.datos['fecha'][2], -1)}, at {briefing_hora} at Machu Picchu Reservations.</td>
            </tr>
            <tr>
                <td style='font-weight: bold; color: #87CEFA;'>N° PERSON:</td>
                <td style='color: #333;'>{len(self.datos['nombres']):02}</td>
            </tr>
        </table>

        <ul style='margin-left: 40px; color: #333;'>
            {''.join([f"<li>{i+1}. {nombre.strip().upper()}</li>" for i, nombre in enumerate(self.datos['nombres'])])}
        </ul>

        <p class='block header'>TOUR INCLUSIONS:</p>
        <ul style='margin-left: 40px;'>
            <li>Transportation to the trailhead</li>
            <li>2 breakfasts</li>
            <li>2 lunches</li>
            <li>2 dinners</li>
            <li>2-night hostel</li>
        """

        if self.datos['machu_picchu_code'] == "0":
            contenido += "<li style='color: #FF4500;'>NOT INCLUDED: Entrance for MACHU PICCHU</li>"
        else:
            contenido += f"<li>Entrance for MACHU PICCHU</li>"
            contenido += f"<li>MACHU PICCHU CODES: {self.datos['machu_picchu_code']}</li>"

        contenido += """
            <li>Transportation from Hidroeléctrica to Cusco - BY CAR</li>
            <li>Guide</li>
            <li>Biking</li>
            <li>Rafting</li>
            <li>Zipline</li>
        </ul>

        <p class='block header'>WHAT TO PACK:</p>
        <ul style='margin-left: 40px; color: #333;'>
            <li><strong>Essentials:</strong> Passport, student ID (if applicable), 25-30L backpack.</li>
            <li><strong>Clothing:</strong> Wool hat/beanie, sun hat, gloves, 2-3 long-sleeve t-shirts, sweater/fleece, 2 pairs pants/leggings, hiking shoes, 1-2 pairs wool socks, rain gear (jacket/pants/poncho), sandals/flip-flops, bath linen/towel.</li>
            <li><strong>Toiletries/Health:</strong> Toothbrush, toothpaste, sunscreen, insect repellent, personal medications.</li>
            <li><strong>Extras:</strong> Snacks (chocolate, nuts, etc.), extra cash in Soles.</li>
            <li><strong>Note:</strong> Pack light; no luggage transfer, but backpacks can be secured during activities.</li>
        </ul>

        <p class='block header'>ITINERARY SUMMARY:</p>
        <p style='text-align: center;'><a href='https://www.machupicchureservations.org/tour/inca-jungle-trail-3-days#itinerary' target='_blank' style='text-decoration: none; color: #87CEFA; font-weight: bold; padding: 8px 16px; border: 2px solid #87CEFA; border-radius: 5px;'>FULL ITINERARY</a></p>
        
        <ul style='margin-left: 40px; color: #333;'>
            <li><strong>Day 01 - Cusco to Santa Teresa:</strong><br>
                  • <span style='color: #FFB6C1;'>Start:</span> Pick-up 6:00 AM from Cusco hotel; 2-hr drive to Ollantaytambo (breakfast)<br>
                  • <span style='color: #FFB6C1;'>Travel:</span> Drive to Abra Malaga (4,350 m)<br>
                  • <span style='color: #FFB6C1;'>Activities:</span> 65 km / 3-4 hr downhill biking to Santa Maria (1,430 m); visit Huamanmarca; 1-1.5 hr rafting; 1-hr car to Santa Teresa<br>
                  • <span style='color: #FFB6C1;'>Stay:</span> Hotel in Santa Teresa<br>
                  • <span style='color: #FFB6C1;'>Meals:</span> Breakfast, Lunch, Dinner<br>
                  • <span style='color: #FFB6C1;'>Difficulty:</span> Moderate<br>
                  • <span style='color: #FFB6C1;'>Weather:</span> Warm, windy
            </li>
            <li><strong>Day 02 - Santa Teresa to Aguas Calientes:</strong><br>
                  • <span style='color: #FFB6C1;'>Start:</span> Breakfast 6:30 AM; pick-up 8:00 AM<br>
                  • <span style='color: #FFB6C1;'>Activities:</span> 2-hr ziplining (4 lines, suspension bridge); 1-hr car ride to Hidroelectrica (lunch)<br>
                  • <span style='color: #FFB6C1;'>Hike:</span> 11 km / 3-3.5 hrs along train tracks to Aguas Calientes<br>
                  • <span style='color: #FFB6C1;'>Stay:</span> Hotel in Aguas Calientes<br>
                  • <span style='color: #FFB6C1;'>Meals:</span> Breakfast, Lunch, Dinner (7:00 PM)<br>
                  • <span style='color: #FFB6C1;'>Difficulty:</span> Moderate<br>
                  • <span style='color: #FFB6C1;'>Weather:</span> Warm, tropical
            </li>
            <li><strong>Day 03 - Machu Picchu & Car Return:</strong><br>
                  • <span style='color: #FFB6C1;'>Start:</span> Wake 4:00 AM; breakfast; hike (1.5 hrs) or bus ($12, 30 min) to Machu Picchu (5:30 AM)<br>
                  • <span style='color: #FFB6C1;'>Activities:</span> 2.5-hr guided tour (Circuit 01/02 preferred)<br>
                  • <span style='color: #FFB6C1;'>Return:</span> Hike to Hidroeléctrica (3-3.5 hrs, leave 10:30 AM); car to Cusco (2:30 PM, 6 hrs, ~9:30 PM)<br>
                  • <span style='color: #FFB6C1;'>Meals:</span> Breakfast<br>
                  • <span style='color: #FFB6C1;'>Note:</span> No time for mountain hikes; extra night recommended.
            </li>
        </ul>
        """

        if self.datos['balance'] > 0:
            contenido += f"""
            <p class='block header'>PAYMENT DETAILS:</p>
            <p style='color: #333;'>Outstanding Balance: ${self.datos['balance']}. Pay online via WeTravel (2.9% fee) or in-person at our Cusco office (cash: no fee; card: 3.9% fee) before the briefing.</p>
            <p style='font-weight: bold; color: #FF4500;'>IMPORTANT: Pay up to one day before the briefing.</p>
            """

        contenido += f"""
        <p class='block header'>OFFICE ADDRESS:</p>
        <p style='font-family: Verdana, sans-serif; color: #333;'>Portal Nuevo 270 Plaza Regocijo - Machu Picchu Reservations: <br> 
        <a href='https://maps.app.goo.gl/XcfipVKjbuLeY3no9' style='color: #FF69B4; font-weight: bold;'>👉(Google Maps)👈</a></p>

        <div style='border-left: 4px solid #98FB98; padding-left: 15px; margin-top: 20px;'>
            <p class='block important'>IMPORTANT:</p>
            <p style='color: #333;'>Please reply to this email with passport photos and your entry date into Peru.</p>
        </div>

        <p class='block header'>DETAILS YOU SHOULD KNOW:</p>
        <ul style='margin-left: 40px; color: #333;'>
            <li>Max 3 hrs at Machu Picchu; circuits 01/02 preferred (<a href='https://www.machupicchureservations.org/destination/machu-picchu-circuits' style='color: #87CEFA;'>details</a>).</li>
            <li>No time for Huayna Picchu/Machu Picchu Mountain with car return.</li>
            <li>Bus tickets to Machu Picchu ($12) not included; arrange night before or morning of.</li>
        </ul>

        <p style='color: #333; margin-top: 20px;'>If you have any questions or need assistance, please contact <a href='https://wa.me/51908851429' 
        style='color: #FF69B4; font-weight: bold;'>👉MPR👈</a>. Contact for additional info or options.</p>

        <div style='color: #333; font-size: 12px; margin-top: 20px;'>
            <h2 style='color: #87CEFA; font-size: 16px;'>MACHUPICCHU RESERVATIONS</h2>
            <p><strong>Schedule:</strong> 7:00-22:00 hrs, Mon-Sat<br><strong>WhatsApp:</strong> <a href='https://api.whatsapp.com/send/?phone=51908851429' style='color: #FF69B4; font-weight: bold;'>👉MPR👈</a></p>
        </div>
        """

        self.mostrar_confirmacion_en_html(contenido)

    def mostrar_confirmacion_en_html(self, contenido):
        nombre_archivo = "confirmacion.html"
        with open(nombre_archivo, "w", encoding="utf-8") as file:
            file.write(f"""
            <html>
            <head>
                <title>Confirmación de Reserva</title>
                <style>
                    body {{ font-family: 'Verdana', sans-serif; margin: 20px; color: #333; }}
                    p {{ line-height: 1.6; font-size: 14px; }}
                    ul {{ list-style-type: none; padding-left: 0; }}
                    ul li::before {{ content: "•"; color: #FFB6C1; font-weight: bold; display: inline-block; width: 1em; margin-left: -1em; }}
                    .important {{ font-weight: bold; color: #FF69B4; }}
                    .header {{ font-size: 16px; font-weight: bold; color: #87CEFA; }}
                </style>
            </head>
            <body>
                {contenido}
            </body>
            </html>
            """)
        print(f"Confirmación guardada como {nombre_archivo}")

class MachuPicchuFullDay:
    def __init__(self, datos):
        self.datos = datos
        self.vistadome_ida = datos.get("vistadome_ida", False)
        self.vistadome_retorno = datos.get("vistadome_retorno", False)

    def generar_confirmacion(self):
        tour = 'MACHU PICCHU FULL DAY BY TRAIN'
        tour_dias = 0
        primer_nombre = self.datos['nombres'][0].split()[0].capitalize()

        contenido = f"""
        <p style='color: #333;'>Dear {primer_nombre},</p>
        <p style='color: #333;'>Your reservation is confirmed - <span style='color: #FF69B4; font-weight: bold;'>{tour}</span></p>
        
        <table>
            <tr>
                <td style='font-weight: bold; color: #FF69B4;'>START DATE:</td>
                <td style='color: #333;'>{fecha_nombre(self.datos['fecha'][0], self.datos['fecha'][1], self.datos['fecha'][2])}</td>
            </tr>
            <tr>
                <td style='font-weight: bold; color: #32CD32;'>BRIEFING DATE:</td>
                <td style='color: #333;'>{fecha_nombre(self.datos['fecha'][0], self.datos['fecha'][1], self.datos['fecha'][2], -1)}, at Machu Picchu Reservations office.</td>
            </tr>
            <tr>
                <td style='font-weight: bold; color: #32CD32;'></td>
                <td style='color: #333;'>Visit the office between 7:00 AM and 10:00 PM to pick up your tickets.</td>
            </tr>
            <tr>
                <td style='font-weight: bold; color: #FF69B4;'>N° PERSON:</td>
                <td style='color: #333;'>{len(self.datos['nombres']):02}</td>
            </tr>
        </table>

        <ul style='margin-left: 40px; color: #333;'>
            {''.join([f"<li>{i+1}. {nombre.strip().upper()}</li>" for i, nombre in enumerate(self.datos['nombres'])])}
        </ul>

        <p class='block header'>WHAT IS INCLUDED:</p>
        <ul style='margin-left: 40px;'>
            <li>Round trip transfer - Cusco - Ollantaytambo - Cusco</li>
            {"<li>Train from Ollantaytambo to Aguas Calientes - BY TRAIN VISTADOME</li>" if self.vistadome_ida else "<li>Train from Ollantaytambo to Aguas Calientes - BY TRAIN</li>"}
            {"<li>Train from Aguas Calientes to Ollantaytambo - BY TRAIN VISTADOME</li>" if self.vistadome_retorno else "<li>Train from Aguas Calientes to Ollantaytambo - BY TRAIN</li>"}
            <li>Round trip tourist bus - Aguas Calientes - Machu Picchu - Aguas Calientes</li>
            {"<li style='color: #FF4500;'>NOT INCLUDED: Entrance for MACHU PICCHU</li>" if self.datos['machu_picchu_code'] == "0" else f"<li>Entrance for MACHU PICCHU</li><li>MACHU PICCHU CODES: {self.datos['machu_picchu_code']}</li>"}
            {f"<li>Entrance for {self.datos['montaña']}</li>" if self.datos.get('montaña', '0') != '0' else ""}
            <li>Guided tour in Machu Picchu</li>
        </ul>

        <p class='block header'>WHAT TO PACK:</p>
        <ul style='margin-left: 40px; color: #333;'>
            <li><strong>Documents:</strong> Passport, student card (if applicable), printed or digital tickets.</li>
            <li><strong>Essentials:</strong> Daypack, 2L water bottle, snacks (apples, cereal bars, sweets, chocolate), camera, cash in Soles (for meals, tips).</li>
            <li><strong>Clothing:</strong> Wool hat/beanie, sun hat, t-shirt, layering item (sweater/fleece), waterproof/windproof jacket (or rain poncho), pants, sturdy walking shoes, sunglasses, gloves.</li>
            <li><strong>Protection:</strong> High SPF sunscreen, insect repellent.</li>
            <li><strong>Note:</strong> Pack light for a comfortable day trip; check weather forecast.</li>
        </ul>

        <p class='block header'>ITINERARY SUMMARY:</p>
        <p style='text-align: center;'><a href='https://www.machupicchureservations.org/tour/machu-picchu-full-day-tour#itinerary' target='_blank' style='text-decoration: none; color: #FF69B4; font-weight: bold; padding: 8px 16px; border: 2px solid #FF69B4; border-radius: 5px;'>FULL ITINERARY</a></p>
        
        <ul style='margin-left: 40px; color: #333;'>
            <li><strong>Day 01 - Cusco to Machu Picchu & Return:</strong><br>
                  • <span style='color: #FFD700;'>Start:</span> Pick-up 4:00-4:15 AM from Cusco hotel; 1 hr 45 min drive to Ollantaytambo<br>
                  • <span style='color: #FFD700;'>Travel:</span> Train to Aguas Calientes (6:10/6:40 AM, 1.5 hrs); arrive ~8:00 AM<br>
                  • <span style='color: #FFD700;'>Ascent:</span> 30-min bus to Machu Picchu (arrive 9:00-10:00 AM)<br>
                  • <span style='color: #FFD700;'>Activities:</span> 2.5-hr guided tour (Circuit 01/02 preferred); free time to explore<br>
                  • <span style='color: #FFD700;'>Return:</span> Bus to Aguas Calientes (25 min); leisure time; train to Ollantaytambo (2:30/3:20 PM, 1.5 hrs); car to Cusco (1 hr 45 min, ~6:30-7:00 PM)<br>
            </li>
        </ul>
        """

        if self.datos['balance'] > 0:
            contenido += f"""
            <p class='block header'>PAYMENT DETAILS:</p>
            <p style='color: #333;'>Outstanding Balance: ${self.datos['balance']}. Pay online via WeTravel (2.9% fee) or in-person at our Cusco office (cash: no fee; card: 3.9% fee) before the trip.</p>
            <p style='font-weight: bold; color: #FF1493;'>IMPORTANT: Pay up to one day before departure.</p>
            """

        contenido += f"""
        <p class='block header'>OFFICE ADDRESS:</p>
        <p style='font-family: Verdana, sans-serif; color: #333;'>Portal Nuevo 270 Plaza Regocijo - Machu Picchu Reservations: <br> 
        <a href='https://maps.app.goo.gl/XcfipVKjbuLeY3no9' style='color: #32CD32; font-weight: bold;'>👉(Google Maps)👈</a></p>

        <div style='border-left: 4px solid #E6E6FA; padding-left: 15px; margin-top: 20px;'>
            <p class='block important'>IMPORTANT:</p>
            <p style='color: #333;'>Please reply to this email with passport photos and your entry date into Peru.</p>
        </div>

        <p class='block header'>DETAILS YOU SHOULD KNOW:</p>
        <ul style='margin-left: 40px; color: #333;'>
            <li>Meals not included; plan for lunch in Aguas Calientes.</li>
        </ul>

        <p style='color: #333; margin-top: 20px;'>If you have any questions or need assistance, please contact <a href='https://wa.me/51908851429' 
        style='color: #32CD32; font-weight: bold;'>👉MPR👈</a>. Contact for additional info or options.</p>

        <div style='color: #333; font-size: 12px; margin-top: 20px;'>
            <h2 style='color: #FF69B4; font-size: 16px;'>MACHUPICCHU RESERVATIONS</h2>
            <p><strong>Schedule:</strong> 7:00-22:00 hrs, Mon-Sat<br><strong>WhatsApp:</strong> <a href='https://api.whatsapp.com/send/?phone=51908851429' style='color: #32CD32; font-weight: bold;'>👉MPR👈</a></p>
        </div>
        """

        self.mostrar_confirmacion_en_html(contenido)

    def mostrar_confirmacion_en_html(self, contenido):
        nombre_archivo = "confirmacion.html"
        with open(nombre_archivo, "w", encoding="utf-8") as file:
            file.write(f"""
            <html>
            <head>
                <title>Confirmación de Reserva</title>
                <style>
                    body {{ font-family: 'Verdana', sans-serif; margin: 20px; color: #333; }}
                    p {{ line-height: 1.6; font-size: 14px; }}
                    ul {{ list-style-type: none; padding-left: 0; }}
                    ul li::before {{ content: "•"; color: #FFD700; font-weight: bold; display: inline-block; width: 1em; margin-left: -1em; }}
                    .important {{ font-weight: bold; color: #32CD32; }}
                    .header {{ font-size: 16px; font-weight: bold; color: #FF69B4; }}
                </style>
            </head>
            <body>
                {contenido}
            </body>
            </html>
            """)
        print(f"Confirmación guardada como {nombre_archivo}")

class MachuPicchu2DTrain:
    def __init__(self, datos):
        self.datos = datos
        self.vistadome_ida = datos.get("vistadome_ida", False)
        self.vistadome_retorno = datos.get("vistadome_retorno", False)

    def generar_confirmacion(self):
        tour = 'MACHU PICCHU 2D-1N TOUR BY TRAIN'
        tour_dias = 1
        primer_nombre = self.datos['nombres'][0].split()[0].capitalize()

        contenido = f"""
        <p style='color: #333;'>Dear {primer_nombre},</p>
        <p style='color: #333;'>Your reservation is confirmed - <span style='color: #20B2AA; font-weight: bold;'>{tour}</span></p>
        
        <table>
            <tr>
                <td style='font-weight: bold; color: #20B2AA;'>START DATE:</td>
                <td style='color: #333;'>{fecha_nombre(self.datos['fecha'][0], self.datos['fecha'][1], self.datos['fecha'][2])}</td>
            </tr>
            <tr>
                <td style='font-weight: bold; color: #20B2AA;'>RETURN DATE:</td>
                <td style='color: #333;'>{fecha_nombre(self.datos['fecha'][0], self.datos['fecha'][1], self.datos['fecha'][2], tour_dias)}</td>
            </tr>
            <tr>
                <td style='font-weight: bold; color: #FF4500;'>BRIEFING DATE:</td>
                <td style='color: #333;'>{fecha_nombre(self.datos['fecha'][0], self.datos['fecha'][1], self.datos['fecha'][2], -1)}, at Machu Picchu Reservations office.</td>
            </tr>
            <tr>
                <td style='font-weight: bold; color: #FF4500;'></td>
                <td style='color: #333;'>Visit the office between 7:00 AM and 10:00 PM to pick up your tickets.</td>
            </tr>
            <tr>
                <td style='font-weight: bold; color: #20B2AA;'>N° PERSON:</td>
                <td style='color: #333;'>{len(self.datos['nombres']):02}</td>
            </tr>
        </table>

        <ul style='margin-left: 40px; color: #333;'>
            {''.join([f"<li>{i+1}. {nombre.strip().upper()}</li>" for i, nombre in enumerate(self.datos['nombres'])])}
        </ul>

        <p class='block header'>TOUR INCLUSIONS:</p>
        <ul style='margin-left: 40px;'>
            <li>Transfer service from your hotel in Cusco to Ollantaytambo train station</li>
            {"<li>Train from Ollantaytambo to Aguas Calientes - BY TRAIN VISTADOME</li>" if self.vistadome_ida else "<li>Train from Ollantaytambo to Aguas Calientes - BY TRAIN</li>"}
            <li>Hostel night in Aguas Calientes town</li>
            <li>Bus tickets from Aguas Calientes to Machu Picchu</li>
            {"<li style='color: #FF4500;'>NOT INCLUDED: Entrance for MACHU PICCHU</li>" if self.datos['machu_picchu_code'] == "0" else f"<li>Entrance for MACHU PICCHU</li><li>MACHU PICCHU CODES: {self.datos['machu_picchu_code']}</li>"}
            {f"<li>Entrance for {self.datos['montaña']}</li>" if self.datos.get('montaña', '0') != '0' else ""}
            <li>Guided service in Machu Picchu</li>
            {"<li>Train from Aguas Calientes to Ollantaytambo - BY TRAIN VISTADOME</li>" if self.vistadome_retorno else "<li>Train from Aguas Calientes to Ollantaytambo - BY TRAIN</li>"}
            <li>Transfer service from Ollantaytambo to Cusco city</li>
        </ul>

        <p class='block header'>NOT INCLUDED:</p>
        <ul style='margin-left: 40px;'>
            <li>Meals</li>
            <li>Extra expenses</li>
        </ul>

        <p class='block header'>WHAT TO PACK:</p>
        <ul style='margin-left: 40px; color: #333;'>
            <li><strong>Essentials:</strong> Original passport, student card (if applicable), small daypack, camera, 2L water, snacks (apples, cereal bars, sweets, chocolate), face mask.</li>
            <li><strong>Clothing:</strong> Wool hat/beanie, sun hat, t-shirt, sweater/fleece, waterproof jacket (or rain poncho), pants, hiking shoes/sneakers, sunglasses, gloves.</li>
            <li><strong>Protection:</strong> Sunscreen, mosquito repellent.</li>
            <li><strong>Extras:</strong> Cash in Soles (for meals, extras).</li>
            <li><strong>Note:</strong> Pack light for overnight stay; bring comfortable layers.</li>
        </ul>

        <p class='block header'>ITINERARY SUMMARY:</p>
        <p style='text-align: center;'><a href='https://www.machupicchureservations.org/tour/machu-picchu-train-2d-1n#itinerary' target='_blank' style='text-decoration: none; color: #20B2AA; font-weight: bold; padding: 8px 16px; border: 2px solid #20B2AA; border-radius: 5px;'>FULL ITINERARY</a></p>
        
        <ul style='margin-left: 40px; color: #333;'>
            <li><strong>Day 01 - Cusco to Aguas Calientes:</strong><br>
                  • <span style='color: #ADFF2F;'>Start:</span> Pick-up 10:00 AM from Cusco hotel; 1 hr 45 min transfer to Ollantaytambo<br>
                  • <span style='color: #ADFF2F;'>Travel:</span> Train to Aguas Calientes (12:55 PM, 1.5 hrs)<br>
                  • <span style='color: #ADFF2F;'>Evening:</span> Check into hotel; briefing with guide (~7:00 PM)<br>
                  • <span style='color: #ADFF2F;'>Stay:</span> Hostel in Aguas Calientes<br>
            </li>
            <li><strong>Day 02 - Machu Picchu & Return:</strong><br>
                  • <span style='color: #ADFF2F;'>Start:</span> Breakfast 5:00 AM; 30-min bus to Machu Picchu (arrive 6:00 AM)<br>
                  • <span style='color: #ADFF2F;'>Activities:</span> 2.5-hr guided tour<br>
                  • <span style='color: #ADFF2F;'>Return:</span> Bus to Aguas Calientes; train to Ollantaytambo (2:30/2:55 PM, 1.5 hrs); car to Cusco (1 hr 45 min, arrive evening)<br>
            </li>
        </ul>
        """

        if self.datos['balance'] > 0:
            contenido += f"""
            <p class='block header'>PAYMENT DETAILS:</p>
            <p style='color: #333;'>Outstanding Balance: ${self.datos['balance']}. Pay online via WeTravel (2.9% fee) or in-person at our Cusco office (cash: no fee; card: 3.9% fee) before the trip.</p>
            <p style='font-weight: bold; color: #00CED1;'>IMPORTANT: Pay up to one day before departure.</p>
            """

        contenido += f"""
        <p class='block header'>OFFICE ADDRESS:</p>
        <p style='font-family: Verdana, sans-serif; color: #333;'>Portal Nuevo 270 Plaza Regocijo - Machu Picchu Reservations: <br> 
        <a href='https://maps.app.goo.gl/XcfipVKjbuLeY3no9' style='color: #FF4500; font-weight: bold;'>👉(Google Maps)👈</a></p>

        <div style='border-left: 4px solid #F0E68C; padding-left: 15px; margin-top: 20px;'>
            <p class='block important'>IMPORTANT:</p>
            <p style='color: #333;'>Please reply to this email with passport photos and your entry date into Peru.</p>
        </div>

        <p class='block header'>DETAILS YOU SHOULD KNOW:</p>
        <ul style='margin-left: 40px; color: #333;'>
            <li>Meals not included; plan for Aguas Calientes.</li>
        </ul>

        <p style='color: #333; margin-top: 20px;'>If you have any questions or need assistance, please contact <a href='https://wa.me/51908851429' 
        style='color: #FF4500; font-weight: bold;'>👉MPR👈</a>. Contact for additional info or options.</p>

        <div style='color: #333; font-size: 12px; margin-top: 20px;'>
            <h2 style='color: #20B2AA; font-size: 16px;'>MACHUPICCHU RESERVATIONS</h2>
            <p><strong>Schedule:</strong> 7:00-22:00 hrs, Mon-Sat<br><strong>WhatsApp:</strong> <a href='https://api.whatsapp.com/send/?phone=51908851429' style='color: #FF4500; font-weight: bold;'>👉MPR👈</a></p>
        </div>
        """

        self.mostrar_confirmacion_en_html(contenido)

    def mostrar_confirmacion_en_html(self, contenido):
        nombre_archivo = "confirmacion.html"
        with open(nombre_archivo, "w", encoding="utf-8") as file:
            file.write(f"""
            <html>
            <head>
                <title>Confirmación de Reserva</title>
                <style>
                    body {{ font-family: 'Verdana', sans-serif; margin: 20px; color: #333; }}
                    p {{ line-height: 1.6; font-size: 14px; }}
                    ul {{ list-style-type: none; padding-left: 0; }}
                    ul li::before {{ content: "•"; color: #ADFF2F; font-weight: bold; display: inline-block; width: 1em; margin-left: -1em; }}
                    .important {{ font-weight: bold; color: #FF4500; }}
                    .header {{ font-size: 16px; font-weight: bold; color: #20B2AA; }}
                </style>
            </head>
            <body>
                {contenido}
            </body>
            </html>
            """)
        print(f"Confirmación guardada como {nombre_archivo}")

class SacredValleyMachuPicchu2D:
    def __init__(self, datos):
        self.datos = datos
        self.vistadome_ida = datos.get("vistadome_ida", False)
        self.vistadome_retorno = datos.get("vistadome_retorno", False)

    def generar_confirmacion(self):
        tour = 'SACRED VALLEY AND MACHU PICCHU 2D-1N'
        tour_dias = 1
        primer_nombre = self.datos['nombres'][0].split()[0].capitalize()

        contenido = (
            f"<p style='color: #333;'>Dear {primer_nombre},</p>"
            f"<p style='color: #333;'>Your reservation is confirmed - <span style='color: #DA70D6; font-weight: bold;'>{tour}</span></p>"
            f"<table>"
            f"<tr><td style='font-weight: bold; color: #DA70D6;'>START DATE:</td><td style='color: #333;'>{fecha_nombre(self.datos['fecha'][0], self.datos['fecha'][1], self.datos['fecha'][2])}</td></tr>"
            f"<tr><td style='font-weight: bold; color: #DA70D6;'>RETURN DATE:</td><td style='color: #333;'>{fecha_nombre(self.datos['fecha'][0], self.datos['fecha'][1], self.datos['fecha'][2], tour_dias)}</td></tr>"
            f"<tr><td style='font-weight: bold; color: #FFA500;'>BRIEFING DATE:</td><td style='color: #333;'>{fecha_nombre(self.datos['fecha'][0], self.datos['fecha'][1], self.datos['fecha'][2], -1)}, at Machu Picchu Reservations office.</td></tr>"
            f"<tr><td style='font-weight: bold; color: #FFA500;'></td><td style='color: #333;'>Visit the office between 7:00 AM and 10:00 PM to pick up your tickets.</td></tr>"
            f"<tr><td style='font-weight: bold; color: #DA70D6;'>N° PERSON:</td><td style='color: #333;'>{len(self.datos['nombres']):02}</td></tr>"
            f"</table>"
        )

        contenido += '<ul style="margin-left: 40px; color: #333;">' + ''.join([f"<li>{i+1}. {nombre.strip().upper()}</li>" for i, nombre in enumerate(self.datos['nombres'])]) + '</ul>'
        contenido += '<p class="block header">TOUR INCLUSIONS:</p><ul style="margin-left: 40px;">'
        contenido += '<li>Sacred Valley tour (Guide + transportation + entrances + buffet lunch)</li>'
        if self.vistadome_ida:
            contenido += '<li>Train from Ollantaytambo to Aguas Calientes - BY TRAIN VISTADOME</li>'
        else:
            contenido += '<li>Train from Ollantaytambo to Aguas Calientes - BY TRAIN</li>'
        contenido += '<li>Round trip bus, Aguas Calientes - Machu Picchu - Aguas Calientes</li>'
        contenido += '<li>01 Hotel in Aguas Calientes</li>'
        if self.datos['machu_picchu_code'] == "0":
            contenido += "<li style='color: #FF4500;'>NOT INCLUDED: Entrance for MACHU PICCHU</li>"
        else:
            contenido += f"<li>Entrance for MACHU PICCHU</li><li>MACHU PICCHU CODES: {self.datos['machu_picchu_code']}</li>"
        if self.datos.get('montaña', '0') != '0':
            contenido += f"<li>Entrance for {self.datos['montaña']}</li>"
        contenido += '<li>Guided tour for Machu Picchu</li>'
        if self.vistadome_retorno:
            contenido += '<li>Train from Aguas Calientes Town to Ollantaytambo - BY TRAIN VISTADOME</li>'
        else:
            contenido += '<li>Train from Aguas Calientes Town to Ollantaytambo - BY TRAIN</li>'
        contenido += '<li>Transfer from Ollantaytambo to Cusco</li></ul>'
        
        contenido += '<p class="block header">NOT INCLUDED:</p><ul style="margin-left: 40px;">'
        contenido += '<li>Meals (except buffet lunch on Day 1)</li>'
        contenido += '<li>Extra expenses</li></ul>'

        contenido += f"""
        <p class='block header'>WHAT TO PACK:</p>
        <ul style='margin-left: 40px; color: #333;'>
            <li><strong>Documents:</strong> Original passport, student card (if applicable).</li>
            <li><strong>Essentials:</strong> Day pack, water bottle, snacks, camera.</li>
            <li><strong>Clothing:</strong> Coat/jacket, t-shirts (2+), cap/hat, sunglasses, tennis shoes/hiking boots, rain poncho.</li>
            <li><strong>Protection:</strong> Sunscreen, insect repellent.</li>
            <li><strong>Extras:</strong> Cash in Soles (for meals, souvenirs).</li>
        </ul>

        <p class='block header'>ITINERARY SUMMARY:</p>
        <p style='text-align: center;'><a href='https://www.machupicchureservations.org/tour/sacred-valley-and-machu-picchu#itinerary' target='_blank' style='text-decoration: none; color: #DA70D6; font-weight: bold; padding: 8px 16px; border: 2px solid #DA70D6; border-radius: 5px;'>FULL ITINERARY</a></p>
        
        <ul style='margin-left: 40px; color: #333;'>
            <li><strong>Day 01 - Sacred Valley & Aguas Calientes:</strong><br>
                  • <span style='color: #98FB98;'>Start:</span> Pick-up 6:30-7:00 AM from Cusco hotel; 45-min drive to Chinchero<br>
                  • <span style='color: #98FB98;'>Activities:</span> Visit Chinchero (site & crafts), Moray terraces, Maras salt mines; buffet lunch in Urubamba (~1:00 PM); tour Ollantaytambo<br>
                  • <span style='color: #98FB98;'>Travel:</span> Train to Aguas Calientes (3:30/4:30 PM, 1 hr 45 min)<br>
                  • <span style='color: #98FB98;'>Evening:</span> Check into hotel; briefing with guide (7:30 PM)<br>
                  • <span style='color: #98FB98;'>Stay:</span> Hotel in Aguas Calientes<br>
                  • <span style='color: #98FB98;'>Meals:</span> Buffet lunch included<br>
            </li>
            <li><strong>Day 02 - Machu Picchu & Return:</strong><br>
                  • <span style='color: #98FB98;'>Start:</span> Breakfast 5:00 AM; 25-min bus to Machu Picchu (arrive 6:00 AM)<br>
                  • <span style='color: #98FB98;'>Activities:</span> 2.5-hr guided tour; optional Wayna Picchu/Machu Picchu Mountain (pre-booked); 30-min free time<br>
                  • <span style='color: #98FB98;'>Return:</span> Bus to Aguas Calientes; train to Ollantaytambo (2:30/3:20 PM, 1 hr 45 min); 2-hr car to Cusco (~6:30 PM, Plaza Regocijo)<br>
                  • <span style='color: #98FB98;'>Note:</span> Max 3 hrs at Machu Picchu; train times may vary.
            </li>
        </ul>
        """

        if self.datos['balance'] > 0:
            contenido += f"""
            <p class='block header'>PAYMENT DETAILS:</p>
            <p style='color: #333;'>Outstanding Balance: ${self.datos['balance']}. Pay online via WeTravel (2.9% fee) or in-person at our Cusco office (cash: no fee; card: 3.9% fee) before the trip.</p>
            <p style='font-weight: bold; color: #FF6347;'>IMPORTANT: Pay up to one day before departure.</p>
            """

        contenido += f"""
        <p class='block header'>OFFICE ADDRESS:</p>
        <p style='font-family: Verdana, sans-serif; color: #333;'>Portal Nuevo 270 Plaza Regocijo - Machu Picchu Reservations: <br> 
        <a href='https://maps.app.goo.gl/XcfipVKjbuLeY3no9' style='color: #FFA500; font-weight: bold;'>👉(Google Maps)👈</a></p>

        <div style='border-left: 4px solid #FFB6C1; padding-left: 15px; margin-top: 20px;'>
            <p class='block important'>IMPORTANT:</p>
            <p style='color: #333;'>Please reply to this email with passport photos and your entry date into Peru.</p>
        </div>

        <p class='block header'>DETAILS YOU SHOULD KNOW:</p>
        <ul style='margin-left: 40px; color: #333;'>
            <li>Meals not included except Day 1 lunch; plan for Aguas Calientes.</li>
        </ul>

        <p style='color: #333; margin-top: 20px;'>If you have any questions or need assistance, please contact <a href='https://wa.me/51908851429' 
        style='color: #FFA500; font-weight: bold;'>👉MPR👈</a>. Contact for additional info or options.</p>

        <div style='color: #333; font-size: 12px; margin-top: 20px;'>
            <h2 style='color: #DA70D6; font-size: 16px;'>MACHUPICCHU RESERVATIONS</h2>
            <p><strong>Schedule:</strong> 7:00-22:00 hrs, Mon-Sat<br><strong>WhatsApp:</strong> <a href='https://api.whatsapp.com/send/?phone=51908851429' style='color: #FFA500; font-weight: bold;'>👉MPR👈</a></p>
        </div>
        """

        self.mostrar_confirmacion_en_html(contenido)

    def mostrar_confirmacion_en_html(self, contenido):
        nombre_archivo = "confirmacion.html"
        with open(nombre_archivo, "w", encoding="utf-8") as file:
            file.write(f"""
            <html>
            <head>
                <title>Confirmación de Reserva</title>
                <style>
                    body {{ font-family: 'Verdana', sans-serif; margin: 20px; color: #333; }}
                    p {{ line-height: 1.6; font-size: 14px; }}
                    ul {{ list-style-type: none; padding-left: 0; }}
                    ul li::before {{ content: "•"; color: #98FB98; font-weight: bold; display: inline-block; width: 1em; margin-left: -1em; }}
                    .important {{ font-weight: bold; color: #FFA500; }}
                    .header {{ font-size: 16px; font-weight: bold; color: #DA70D6; }}
                </style>
            </head>
            <body>
                {contenido}
            </body>
            </html>
            """)
        print(f"Confirmación guardada como {nombre_archivo}")

#REVISAR ESTA CLASE 
class CuscoCitySacredValleyMachuPicchu3D:
    #sin hora especifica de briefing
    def __init__(self, datos):
        self.datos = datos
        self.vistadome_ida = datos.get("vistadome_ida", False)
        self.vistadome_retorno = datos.get("vistadome_retorno", False)

    def generar_confirmacion(self):
        tour = 'CUSCO CITY, SACRED VALLEY + MACHU PICCHU 3D-2N'
        #briefing_hora = "6:00 PM"
        primer_nombre = self.datos['nombres'][0].split()[0].capitalize()
        tour_dias = 2  # Se usan para calcular la fecha de retorno

        # Generar el contenido de la cabecera
        contenido = (
            f"<p>Dear {primer_nombre},</p>"
            f"<p>Your reservation is confirmed - <span style='color: #1E90FF; font-weight: bold;'>{tour}</span></p>"
            f"<table><tr><td style='font-weight: bold; color: #FF4500;'>START DATE:</td><td>{fecha_nombre(self.datos['fecha'][0], self.datos['fecha'][1], self.datos['fecha'][2])}</td></tr>"
            f"<tr><td style='font-weight: bold; color: #007bff;'>RETURN DATE:</td><td>{fecha_nombre(self.datos['fecha'][0], self.datos['fecha'][1], self.datos['fecha'][2], tour_dias)}</td></tr>"
            f"<tr><td style='font-weight: bold; color: #d9534f;'>BRIEFING DATE:</td><td>{fecha_nombre(self.datos['fecha'][0], self.datos['fecha'][1], self.datos['fecha'][2], -1)}, at Machu Picchu Reservations office.</td></tr>"
            f"<tr><td style='font-weight: bold; color: #d9534f;'></td><td>You must come to the office between 7:00 am and 10:00 pm to pick up all your tickets.</td></tr>"
            f"<tr><td style='font-weight: bold; color: #FF4500;'>N° PERSON:</td><td>{len(self.datos['nombres']):02}</td></tr></table>"
        )

        contenido += '<ul style="margin-left: 40px;">' + ''.join([f"<li>{i+1}. {nombre.strip().upper()}</li>" for i, nombre in enumerate(self.datos['nombres'])]) + '</ul>'
        contenido += '<p style="font-weight: bold; color: #2E8B57;">TOUR INCLUSION:</p><ul style="margin-left: 40px;">'
        contenido += '<li>Cusco City tour (Guide + transportation)</li>'
        contenido += '<li>Sacred Valley tour (Guide + transportation + entrances + lunch)</li>'

        # Añadir información sobre el tren de ida
        if self.vistadome_ida:
            contenido += '<li>Train from Ollantaytambo to Aguas Calientes - BY TRAIN VISTADOME</li>'
        else:
            contenido += '<li>Train from Ollantaytambo to Aguas Calientes - BY TRAIN</li>'

        contenido += '<li>Round trip bus, Aguas Calientes - Machu Picchu - Aguas Calientes</li>'
        contenido += '<li>01 Hotel night in Aguas Calientes</li>'

        # Añadir entrada para Machu Picchu
        if self.datos['machu_picchu_code'] == "0":
            contenido += "<li style='color: #FF4500;'>NOT INCLUDED: Entrance for MACHU PICCHU</li>"
        else:
            contenido += f"<li>Entrance for MACHU PICCHU</li>"
            contenido += f"<li>MACHU PICCHU CODES: {self.datos['machu_picchu_code']}</li>"

        # Añadir información sobre la montaña seleccionada
        if self.datos.get('montaña', '0') != '0':
            contenido += f"<li>Entrance for {self.datos['montaña']}</li>"

        contenido += '<li>Guided tour for Machu Picchu</li>'

        # Añadir información sobre el tren de retorno
        if self.vistadome_retorno:
            contenido += '<li>Train from Aguas Calientes Town to Ollantaytambo - BY TRAIN VISTADOME</li>'
        else:
            contenido += '<li>Train from Aguas Calientes Town to Ollantaytambo - BY TRAIN</li>'

        contenido += '<li>Transfer from Ollantaytambo to Cusco</li></ul>'

        contenido += '<p style="font-weight: bold; color: #B22222;">NOT INCLUDED:</p><ul style="margin-left: 40px;">'
        contenido += '<li>Meals not specified in the itinerary</li>'
        contenido += '<li>Entrance fees for Cusco ruins (not included for the Sacred Valley tour)</li>'
        contenido += '<li>Extra expenses</li></ul>'

        contenido += '<p style="font-weight: bold; color: #2E8B57;">WHAT TO PACK FOR THE TOUR:</p><ul style="margin-left: 40px;">'
        contenido += '<li>A coat for cold weather</li>'
        contenido += '<li>Sunscreen and sunglasses</li>'
        contenido += '<li>Comfortable walking shoes</li>'
        contenido += '<li>Water</li>'
        contenido += '<li>Photographic camera</li>'
        contenido += '<li>Original Passport</li>'
        contenido += '<li>Rain Poncho (plastic)</li></ul>'

        if self.datos['balance'] > 0:
            contenido += f"""
            <p class="block header">Payment Details:</p>
            <p>Outstanding Balance: ${self.datos['balance']}. Make your payment online through WeTravel by clicking the "Manage Your Booking" button in the email you received with your initial reservation payment (a 2.9% fee applies). Alternatively, you can pay in person at our Cusco office before the briefing; cash payments have no additional charges, while card payments are subject to a 3.9% fee.</p>
            <p style="font-weight: bold; color:#ff00fb;">IMPORTANT: We recommend paying the fee up to one day before the briefing.</p>
            """

        # OFICINA, IMPORTANTE, MENSAJE WHATSAPP
        contenido += f"""
            <p class="block header">OFFICE ADDRESS:</p>
            <p style="font-family: Verdana, sans-serif;">Portal Nuevo 270 Plaza Regocijo - Machu Picchu Reservations: <br> 
            Office address link: <a href="https://maps.app.goo.gl/XcfipVKjbuLeY3no9" 
            style="text-decoration: underline; color: #ff0000; font-weight: bold;">👉(Google Maps)👈</a></p>
            
            <div style="border-left: 4px solid #ff6600; padding-left: 15px; margin-top: 20px;">
                <p class="block important" style="font-family: Verdana, sans-serif; font-size: 16px; font-weight: bold; color: #d9534f;">IMPORTANT:</p>
                <p style="font-family: Verdana, sans-serif; color:#333; font-size: 14px;">
                    Please reply to this email by sending your photos of your passports and <strong>inform us of your entry date into the country</strong>. Additionally, <strong>attach the Andean Migration Card</strong> once provided by the Migration Office. These details are essential for <strong>tax and administrative matters (SUNAT)</strong>. 
                </p>
            </div>
        """

        # REVISAR DATOS
        contenido += f"""
            <div style="border-left: 4px solid #00a20a; padding-left: 15px; margin-top: 20px;">
        """

        if self.datos['machu_picchu_code'] != '0':
            contenido += f"""
                <p style="font-weight: bold; color:#007f00; font-size: 14px; font-family: Verdana, Geneva, sans-serif;">
                    Please double-check that your <strong>name, passport number, and ticket date</strong> are all correct. We will provide you with printed copies of all your tickets on the day of your briefing.
                </p>
            """

        contenido += f"""
                <p style="font-weight: bold; color:#007f00; font-size: 14px; font-family: Verdana, Geneva, sans-serif;">
                    Additionally, please make sure to update the <strong>WhatsApp numbers</strong> of all participants in your reservation on <strong>We Travel</strong>, or feel free to request assistance with registering them if needed.
                </p>
            </div>
        """

        self.mostrar_confirmacion_en_html(contenido)

    def mostrar_confirmacion_en_html(self, contenido):
        nombre_archivo = "confirmacion.html"
        with open(nombre_archivo, "w", encoding="utf-8") as file:
            file.write(f"""
            <html>
            <head>
                <title>Confirmación de Reserva</title>
                <style>
                    body {{
                        font-family: 'Verdana', sans-serif;
                        margin: 20px;
                        color: #2F4F4F;
                    }}
                    p {{
                        line-height: 1.6;
                        font-size: 14px;
                    }}
                    ul {{
                        list-style-type: none;
                        padding-left: 0;
                    }}
                    ul li::before {{
                        content: "•";
                        color: #A52A2A;
                        font-weight: bold;
                        display: inline-block;
                        width: 1em;
                        margin-left: -1em;
                    }}
                    .important {{
                        font-weight: bold;
                        color: #B22222;
                    }}
                    .header {{
                        font-size: 16px;
                        font-weight: bold;
                        color: #556B2F;
                    }}
                    .highlight {{
                        color: #6B8E23;
                        font-weight: bold;
                    }}
                </style>
            </head>
            <body>
                {contenido}
            </body>
            </html>
            """)

        print(f"Confirmación guardada como {nombre_archivo}")

class MachuPicchuByCar2D:
    def __init__(self, datos):
        self.datos = datos

    def generar_confirmacion(self):
        tour = 'MACHU PICCHU BY CAR 2D - 1N'
        tour_dias = 1
        primer_nombre = self.datos['nombres'][0].split()[0].capitalize()

        contenido = f"""
        <p style='color: #333;'>Dear {primer_nombre},</p>
        <p style='color: #333;'>Your reservation is confirmed - <span style='color: #FF4500; font-weight: bold;'>{tour}</span></p>
        
        <table>
            <tr>
                <td style='font-weight: bold; color: #FF4500;'>START DATE:</td>
                <td style='color: #333;'>{fecha_nombre(self.datos['fecha'][0], self.datos['fecha'][1], self.datos['fecha'][2])}</td>
            </tr>
            <tr>
                <td style='font-weight: bold; color: #FF4500;'>RETURN DATE:</td>
                <td style='color: #333;'>{fecha_nombre(self.datos['fecha'][0], self.datos['fecha'][1], self.datos['fecha'][2], tour_dias)}</td>
            </tr>
            <tr>
                <td style='font-weight: bold; color: #00FF7F;'>BRIEFING DATE:</td>
                <td style='color: #333;'>{fecha_nombre(self.datos['fecha'][0], self.datos['fecha'][1], self.datos['fecha'][2], -1)}, at Machu Picchu Reservations office.</td>
            </tr>
            <tr>
                <td style='font-weight: bold; color: #00FF7F;'></td>
                <td style='color: #333;'>Visit the office between 7:00 AM and 10:00 PM to pick up your tickets.</td>
            </tr>
            <tr>
                <td style='font-weight: bold; color: #FF4500;'>N° PERSON:</td>
                <td style='color: #333;'>{len(self.datos['nombres']):02}</td>
            </tr>
        </table>

        <ul style='margin-left: 40px; color: #333;'>
            {''.join([f"<li>{i+1}. {nombre.strip().upper()}</li>" for i, nombre in enumerate(self.datos['nombres'])])}
        </ul>

        <p class='block header'>TOUR INCLUSIONS:</p>
        <ul style='margin-left: 40px;'>
            <li>Transportation: includes transportation to the trailhead and transport back from Hidroelectrica to Cusco</li>
            <li>1 Night of Accommodations: one night in comfortable lodging is provided</li>
            {"<li style='color: #FF4500;'>NOT INCLUDED: Entrance for MACHU PICCHU</li>" if self.datos['machu_picchu_code'] == "0" else f"<li>Entrance for MACHU PICCHU</li><li>MACHU PICCHU CODES: {self.datos['machu_picchu_code']}</li>"}
            {f"<li>Entrance for {self.datos['montaña']}</li>" if self.datos.get('montaña', '0') != '0' else ""}
            <li>Entrance to Machu Picchu: Early access to Machu Picchu at 6:00 AM - 9:00 AM</li>
            <li>A professional Guide: A dedicated professional guide will accompany you throughout your journey, ensuring a memorable experience</li>
            <li>Meals: 1 lunch, 1 dinner, 1 breakfast are included</li>
        </ul>

        <p class='block header'>WHAT TO PACK:</p>
        <ul style='margin-left: 40px; color: #333;'>
            <li><strong>Documents:</strong> Original passport, student card (if applicable).</li>
            <li><strong>Essentials:</strong> Small backpack/daypack, water bottle (1-2L), snacks (energy bars, nuts, dried fruit), camera/smartphone (with charger/batteries).</li>
            <li><strong>Clothing:</strong> Light, breathable, quick-dry layers (t-shirts, long-sleeve shirts), light jacket/fleece, comfortable pants/shorts, waterproof jacket/poncho, underwear, socks (moisture-wicking), sturdy hiking shoes/sneakers, hat/cap, sunglasses.</li>
            <li><strong>Protection:</strong> Sunscreen (SPF 30+), insect repellent.</li>
            <li><strong>Personal:</strong> Wet wipes, small towel, personal medications, basic first-aid kit (band-aids, pain relievers).</li>
            <li><strong>Extras:</strong> Cash in Soles (for extras), hotel reservation details.</li>
            <li><strong>Note:</strong> Pack light; check weather forecast.</li>
        </ul>

        <p class='block header'>ITINERARY SUMMARY:</p>
        <p style='text-align: center;'><a href='https://www.machupicchureservations.org/tour/machu-picchu-tour-by-car-2d-1n#itinerary' target='_blank' style='text-decoration: none; color: #FF4500; font-weight: bold; padding: 8px 16px; border: 2px solid #FF4500; border-radius: 5px;'>FULL ITINERARY</a></p>
        
        <ul style='margin-left: 40px; color: #333;'>
            <li><strong>Day 01 - Cusco to Aguas Calientes:</strong><br>
                  • <span style='color: #87CEFA;'>Start:</span> Meet at Machu Picchu Reservations Office 6:30 AM; 6-hr drive to Hidroelectrica<br>
                  • <span style='color: #87CEFA;'>Activities:</span> Lunch in Hidroelectrica; 11 km / 3-3.5 hr trek to Aguas Calientes<br>
                  • <span style='color: #87CEFA;'>Evening:</span> Check into hotel; dinner in town<br>
                  • <span style='color: #87CEFA;'>Stay:</span> Hotel in Aguas Calientes<br>
                  • <span style='color: #87CEFA;'>Meals:</span> Lunch, Dinner<br>
                  • <span style='color: #87CEFA;'>Weather:</span> Warm, windy, tropical
            </li>
            <li><strong>Day 02 - Machu Picchu & Return:</strong><br>
                  • <span style='color: #87CEFA;'>Start:</span> Breakfast; walk (4 km / 1.5-2 hrs) or bus ($12) to Machu Picchu (arrive 6:00 AM)<br>
                  • <span style='color: #87CEFA;'>Activities:</span> Guided tour; free exploration<br>
                  • <span style='color: #87CEFA;'>Return:</span> 11 km / 3.5 hr trek to Hidroelectrica (start ~10:00 AM); car to Cusco (2:30 PM, 6-7 hrs, arrive evening)<br>
                  • <span style='color: #87CEFA;'>Meals:</span> Breakfast<br>
                  • <span style='color: #87CEFA;'>Weather:</span> Warm, windy, tropical
            </li>
        </ul>
        """

        if self.datos['balance'] > 0:
            contenido += f"""
            <p class='block header'>PAYMENT DETAILS:</p>
            <p style='color: #333;'>Outstanding Balance: ${self.datos['balance']}. Pay online via WeTravel (2.9% fee) or in-person at our Cusco office (cash: no fee; card: 3.9% fee) before the trip.</p>
            <p style='font-weight: bold; color: #FF69B4;'>IMPORTANT: Pay up to one day before departure.</p>
            """

        contenido += f"""
        <p class='block header'>OFFICE ADDRESS:</p>
        <p style='font-family: Verdana, sans-serif; color: #333;'>Portal Nuevo 270 Plaza Regocijo - Machu Picchu Reservations: <br> 
        <a href='https://maps.app.goo.gl/XcfipVKjbuLeY3no9' style='color: #00FF7F; font-weight: bold;'>👉(Google Maps)👈</a></p>

        <div style='border-left: 4px solid #FFD700; padding-left: 15px; margin-top: 20px;'>
            <p class='block important'>IMPORTANT:</p>
            <p style='color: #333;'>Please reply to this email with passport photos and your entry date into Peru.</p>
        </div>

        <p class='block header'>DETAILS YOU SHOULD KNOW:</p>
        <ul style='margin-left: 40px; color: #333;'>
            <li>Max 3 hrs at Machu Picchu; early entry 6:00-9:00 AM.</li>
            <li>Bus to Machu Picchu ($12) optional, not included.</li>
            <li>No mountain hikes included; plan return trek to avoid delays.</li>
        </ul>

        <p style='color: #333; margin-top: 20px;'>If you have any questions or need assistance, please contact <a href='https://wa.me/51908851429' 
        style='color: #00FF7F; font-weight: bold;'>👉MPR👈</a>. Contact for additional info or options.</p>

        <div style='color: #333; font-size: 12px; margin-top: 20px;'>
            <h2 style='color: #FF4500; font-size: 16px;'>MACHUPICCHU RESERVATIONS</h2>
            <p><strong>Schedule:</strong> 7:00-22:00 hrs, Mon-Sat<br><strong>WhatsApp:</strong> <a href='https://api.whatsapp.com/send/?phone=51908851429' style='color: #00FF7F; font-weight: bold;'>👉MPR👈</a></p>
        </div>
        """

        self.mostrar_confirmacion_en_html(contenido)

    def mostrar_confirmacion_en_html(self, contenido):
        nombre_archivo = "confirmacion.html"
        with open(nombre_archivo, "w", encoding="utf-8") as file:
            file.write(f"""
            <html>
            <head>
                <title>Confirmación de Reserva</title>
                <style>
                    body {{ font-family: 'Verdana', sans-serif; margin: 20px; color: #333; }}
                    p {{ line-height: 1.6; font-size: 14px; }}
                    ul {{ list-style-type: none; padding-left: 0; }}
                    ul li::before {{ content: "•"; color: #87CEFA; font-weight: bold; display: inline-block; width: 1em; margin-left: -1em; }}
                    .important {{ font-weight: bold; color: #00FF7F; }}
                    .header {{ font-size: 16px; font-weight: bold; color: #FF4500; }}
                </style>
            </head>
            <body>
                {contenido}
            </body>
            </html>
            """)
        print(f"Confirmación guardada como {nombre_archivo}")

class MachuPicchuByCarTrain2D:
    def __init__(self, datos):
        self.datos = datos

    def generar_confirmacion(self):
        tour = 'MACHU PICCHU BY CAR + BY TRAIN 2D-1N'
        tour_dias = 1
        primer_nombre = self.datos['nombres'][0].split()[0].capitalize()

        contenido = f"""
        <p style='color: #333;'>Dear {primer_nombre},</p>
        <p style='color: #333;'>Your reservation is confirmed - <span style='color: #6A5ACD; font-weight: bold;'>{tour}</span></p>
        
        <table>
            <tr>
                <td style='font-weight: bold; color: #6A5ACD;'>START DATE:</td>
                <td style='color: #333;'>{fecha_nombre(self.datos['fecha'][0], self.datos['fecha'][1], self.datos['fecha'][2])}</td>
            </tr>
            <tr>
                <td style='font-weight: bold; color: #6A5ACD;'>RETURN DATE:</td>
                <td style='color: #333;'>{fecha_nombre(self.datos['fecha'][0], self.datos['fecha'][1], self.datos['fecha'][2], tour_dias)}</td>
            </tr>
            <tr>
                <td style='font-weight: bold; color: #FFD700;'>BRIEFING DATE:</td>
                <td style='color: #333;'>{fecha_nombre(self.datos['fecha'][0], self.datos['fecha'][1], self.datos['fecha'][2], -1)}, at Machu Picchu Reservations office.</td>
            </tr>
            <tr>
                <td style='font-weight: bold; color: #FFD700;'></td>
                <td style='color: #333;'>Visit the office between 7:00 AM and 10:00 PM to pick up your tickets.</td>
            </tr>
            <tr>
                <td style='font-weight: bold; color: #6A5ACD;'>N° PERSON:</td>
                <td style='color: #333;'>{len(self.datos['nombres']):02}</td>
            </tr>
        </table>

        <ul style='margin-left: 40px; color: #333;'>
            {''.join([f"<li>{i+1}. {nombre.strip().upper()}</li>" for i, nombre in enumerate(self.datos['nombres'])])}
        </ul>

        <p class='block header'>TOUR INCLUSIONS:</p>
        <ul style='margin-left: 40px;'>
            <li>TRANSPORTATION FROM CUSCO - HIDROELÉCTRICA</li>
            <li>01 LUNCH</li>
            <li>01 DINNER</li>
            {"<li style='color: #FF4500;'>NOT INCLUDED: Entrance for MACHU PICCHU</li>" if self.datos['machu_picchu_code'] == "0" else f"<li>Entrance for MACHU PICCHU</li><li>MACHU PICCHU CODES: {self.datos['machu_picchu_code']}</li>"}
            {f"<li>Entrance for {self.datos['montaña']}</li>" if self.datos.get('montaña', '0') != '0' else ""}
            <li>01 HOSTEL NIGHT IN AGUAS CALIENTES - ALLPA INN</li>
            <li>GUIDE FOR MACHU PICCHU</li>
            {"<li>TRAIN FROM AGUAS CALIENTES TO OLLANTAYTAMBO - BY TRAIN VISTADOME</li>" if self.datos.get("vistadome_retorno", False) else "<li>TRAIN FROM AGUAS CALIENTES TO OLLANTAYTAMBO - BY TRAIN</li>"}
            <li>TRANSFER FROM OLLANTAYTAMBO TO CUSCO</li>
        </ul>

        <p class='block header'>WHAT TO PACK:</p>
        <ul style='margin-left: 40px; color: #333;'>
            <li><strong>Essentials:</strong> Daypack, original passport, student card (if applicable), water bottle, camera.</li>
            <li><strong>Clothing:</strong> Coat/jacket, quick-dry pants/shorts, moisture-wicking shirts, waterproof jacket/poncho, tennis shoes/hiking boots, hat/cap, sunglasses.</li>
            <li><strong>Protection:</strong> Sunscreen, insect repellent.</li>
            <li><strong>Extras:</strong> Cash in Soles (for meals, souvenirs).</li>
            <li><strong>Note:</strong> Pack light for trek and train; adjust for weather.</li>
        </ul>

        <p class='block header'>ITINERARY SUMMARY:</p>
        <p style='text-align: center;'><a href='https://www.machupicchureservations.org/tour/machu-picchu-tour-by-car-and-by-train-2-days#itinerary' target='_blank' style='text-decoration: none; color: #6A5ACD; font-weight: bold; padding: 8px 16px; border: 2px solid #6A5ACD; border-radius: 5px;'>FULL ITINERARY</a></p>
        
        <ul style='margin-left: 40px; color: #333;'>
            <li><strong>Day 01 - Cusco to Aguas Calientes:</strong><br>
                  • <span style='color: #FFA07A;'>Start:</span> Meet at Machu Picchu Reservations Office 6:30 AM; 6-hr drive to Hidroelectrica<br>
                  • <span style='color: #FFA07A;'>Activities:</span> Lunch in Hidroelectrica; 11 km / 3-3.5 hr trek to Aguas Calientes<br>
                  • <span style='color: #FFA07A;'>Evening:</span> Check into hotel; dinner in town<br>
                  • <span style='color: #FFA07A;'>Stay:</span> Hotel in Aguas Calientes<br>
                  • <span style='color: #FFA07A;'>Meals:</span> Lunch, Dinner<br>
                  • <span style='color: #FFA07A;'>Weather:</span> Warm, windy, tropical
            </li>
            <li><strong>Day 02 - Machu Picchu & Return:</strong><br>
                  • <span style='color: #FFA07A;'>Start:</span> Early rise; walk (1.5-2 hrs) or bus ($12, not included) to Machu Picchu<br>
                  • <span style='color: #FFA07A;'>Activities:</span> Guided tour; free time to explore or visit Sun Gate<br>
                  • <span style='color: #FFA07A;'>Return:</span> Bus/walk to Aguas Calientes; train to Ollantaytambo; car to Cusco (arrive evening)<br>
                  • <span style='color: #FFA07A;'>Weather:</span> Warm, windy, tropical
            </li>
        </ul>
        """

        if self.datos['balance'] > 0:
            contenido += f"""
            <p class='block header'>PAYMENT DETAILS:</p>
            <p style='color: #333;'>Outstanding Balance: ${self.datos['balance']}. Pay online via WeTravel (2.9% fee) or in-person at our Cusco office (cash: no fee; card: 3.9% fee) before the trip.</p>
            <p style='font-weight: bold; color: #FF1493;'>IMPORTANT: Pay up to one day before departure.</p>
            """

        contenido += f"""
        <p class='block header'>OFFICE ADDRESS:</p>
        <p style='font-family: Verdana, sans-serif; color: #333;'>Portal Nuevo 270 Plaza Regocijo - Machu Picchu Reservations: <br> 
        <a href='https://maps.app.goo.gl/XcfipVKjbuLeY3no9' style='color: #FFD700; font-weight: bold;'>👉(Google Maps)👈</a></p>

        <div style='border-left: 4px solid #98FB98; padding-left: 15px; margin-top: 20px;'>
            <p class='block important'>IMPORTANT:</p>
            <p style='color: #333;'>Please reply to this email with passport photos and your entry date into Peru.</p>
        </div>

        <p class='block header'>DETAILS YOU SHOULD KNOW:</p>
        <ul style='margin-left: 40px; color: #333;'>
            <li>Bus to Machu Picchu ($12) not included; walking option available.</li>
            <li>Train times may vary; confirm at briefing.</li>
            <li>No breakfast on Day 2; plan accordingly.</li>
        </ul>

        <p style='color: #333; margin-top: 20px;'>If you have any questions or need assistance, please contact <a href='https://wa.me/51908851429' 
        style='color: #FFD700; font-weight: bold;'>👉MPR👈</a>. Contact for additional info or options.</p>

        <div style='color: #333; font-size: 12px; margin-top: 20px;'>
            <h2 style='color: #6A5ACD; font-size: 16px;'>MACHUPICCHU RESERVATIONS</h2>
            <p><strong>Schedule:</strong> 7:00-22:00 hrs, Mon-Sat<br><strong>WhatsApp:</strong> <a href='https://api.whatsapp.com/send/?phone=51908851429' style='color: #FFD700; font-weight: bold;'>👉MPR👈</a></p>
        </div>
        """

        self.mostrar_confirmacion_en_html(contenido)

    def mostrar_confirmacion_en_html(self, contenido):
        nombre_archivo = "confirmacion.html"
        with open(nombre_archivo, "w", encoding="utf-8") as file:
            file.write(f"""
            <html>
            <head>
                <title>Confirmación de Reserva</title>
                <style>
                    body {{ font-family: 'Verdana', sans-serif; margin: 20px; color: #333; }}
                    p {{ line-height: 1.6; font-size: 14px; }}
                    ul {{ list-style-type: none; padding-left: 0; }}
                    ul li::before {{ content: "•"; color: #FFA07A; font-weight: bold; display: inline-block; width: 1em; margin-left: -1em; }}
                    .important {{ font-weight: bold; color: #FFD700; }}
                    .header {{ font-size: 16px; font-weight: bold; color: #6A5ACD; }}
                </style>
            </head>
            <body>
                {contenido}
            </body>
            </html>
            """)
        print(f"Confirmación guardada como {nombre_archivo}")

class MachuPicchuByCar3D:
    def __init__(self, datos):
        self.datos = datos

    def generar_confirmacion(self):
        tour = 'MACHU PICCHU BY CAR 3D-2N'
        tour_dias = 2
        mp_dia = 1  # Día en que se visita Machu Picchu
        primer_nombre = self.datos['nombres'][0].split()[0].capitalize()

        contenido = f"""
        <p style='color: #333;'>Dear {primer_nombre},</p>
        <p style='color: #333;'>Your reservation is confirmed - <span style='color: #228B22; font-weight: bold;'>{tour}</span></p>
        
        <table>
            <tr>
                <td style='font-weight: bold; color: #228B22;'>START DATE:</td>
                <td style='color: #333;'>{fecha_nombre(self.datos['fecha'][0], self.datos['fecha'][1], self.datos['fecha'][2])}</td>
            </tr>
            <tr>
                <td style='font-weight: bold; color: #228B22;'>MP DATE:</td>
                <td style='color: #333;'>{fecha_nombre(self.datos['fecha'][0], self.datos['fecha'][1], self.datos['fecha'][2], mp_dia)}</td>
            </tr>
            <tr>
                <td style='font-weight: bold; color: #228B22;'>RETURN DATE:</td>
                <td style='color: #333;'>{fecha_nombre(self.datos['fecha'][0], self.datos['fecha'][1], self.datos['fecha'][2], tour_dias)}</td>
            </tr>
            <tr>
                <td style='font-weight: bold; color: #FF69B4;'>BRIEFING DATE:</td>
                <td style='color: #333;'>{fecha_nombre(self.datos['fecha'][0], self.datos['fecha'][1], self.datos['fecha'][2], -1)}, at Machu Picchu Reservations office.</td>
            </tr>
            <tr>
                <td style='font-weight: bold; color: #FF69B4;'></td>
                <td style='color: #333;'>Visit the office between 7:00 AM and 10:00 PM to pick up your tickets.</td>
            </tr>
            <tr>
                <td style='font-weight: bold; color: #228B22;'>N° PERSON:</td>
                <td style='color: #333;'>{len(self.datos['nombres']):02}</td>
            </tr>
        </table>

        <ul style='margin-left: 40px; color: #333;'>
            {''.join([f"<li>{i+1}. {nombre.strip().upper()}</li>" for i, nombre in enumerate(self.datos['nombres'])])}
        </ul>

        <p class='block header'>TOUR INCLUSIONS:</p>
        <ul style='margin-left: 40px;'>
            <li>TRANSPORTATION: CUSCO - HIDROELÉCTRICA</li>
            <li>01 LUNCH</li>
            <li>01 DINNER</li>
            <li>01 BOX LUNCH</li>
            <li>02 HOSTEL NIGHTS IN AGUAS CALIENTES</li>
            {"<li style='color: #FF4500;'>NOT INCLUDED: Entrance for MACHU PICCHU</li>" if self.datos['machu_picchu_code'] == "0" else f"<li>Entrance for MACHU PICCHU</li><li>MACHU PICCHU CODES: {self.datos['machu_picchu_code']}</li>"}
            {f"<li>Entrance for {self.datos['montaña']}</li>" if self.datos.get('montaña', '0') != '0' else ""}
            <li>GUIDE FOR MACHU PICCHU</li>
            <li>TRANSPORTATION: HIDROELÉCTRICA - CUSCO</li>
        </ul>

        <p class='block header'>WHAT TO PACK:</p>
        <ul style='margin-left: 40px; color: #333;'>
            <li><strong>Documents:</strong> Original passport, student card (if applicable).</li>
            <li><strong>Essentials:</strong> Water bottle, camera.</li>
            <li><strong>Clothing:</strong> Warm jacket/coat, rain poncho, tennis shoes/hiking boots, cap/hat, sunglasses.</li>
            <li><strong>Protection:</strong> Sunscreen, insect repellent.</li>
        </ul>

        <p class='block header'>ITINERARY SUMMARY:</p>
        <p style='text-align: center;'><a href='https://www.machupicchureservations.org/tour/machu-picchu-tour-by-car-3-days#itinerary' target='_blank' style='text-decoration: none; color: #228B22; font-weight: bold; padding: 8px 16px; border: 2px solid #228B22; border-radius: 5px;'>FULL ITINERARY</a></p>
        
        <ul style='margin-left: 40px; color: #333;'>
            <li><strong>Day 01 - Cusco to Aguas Calientes:</strong><br>
                  • <span style='color: #40E0D0;'>Start:</span> Meet at Machu Picchu Reservations Office 6:30 AM; 6-hr drive to Hidroelectrica<br>
                  • <span style='color: #40E0D0;'>Activities:</span> Lunch in Hidroelectrica; 3-hr trek to Aguas Calientes<br>
                  • <span style='color: #40E0D0;'>Evening:</span> Check into hostel; dinner and briefing with guide<br>
                  • <span style='color: #40E0D0;'>Stay:</span> Hostel in Aguas Calientes<br>
                  • <span style='color: #40E0D0;'>Meals:</span> Lunch, Dinner
            </li>
            <li><strong>Day 02 - Machu Picchu Exploration:</strong><br>
                  • <span style='color: #40E0D0;'>Start:</span> Walk (start 4:00 AM) or bus ($12, not included) to Machu Picchu (arrive 6:00 AM)<br>
                  • <span style='color: #40E0D0;'>Activities:</span> Guided tour; free time to explore or climb Machu Picchu Mountain/Huayna Picchu<br>
                  • <span style='color: #40E0D0;'>Stay:</span> Hostel in Aguas Calientes<br>
                  • <span style='color: #40E0D0;'>Meals:</span> Box lunch
            </li>
            <li><strong>Day 03 - Return to Cusco:</strong><br>
                  • <span style='color: #40E0D0;'>Start:</span> Trek to Hidroelectrica (~9:30 AM, 3 hrs, arrive by 2:00 PM)<br>
                  • <span style='color: #40E0D0;'>Return:</span> 7-hr drive to Cusco (depart 2:30 PM, arrive 9:00-10:00 PM, Plaza Regocijo)
            </li>
        </ul>
        """

        if self.datos['balance'] > 0:
            contenido += f"""
            <p class='block header'>PAYMENT DETAILS:</p>
            <p style='color: #333;'>Outstanding Balance: ${self.datos['balance']}. Pay online via WeTravel (2.9% fee) or in-person at our Cusco office (cash: no fee; card: 3.9% fee) before the trip.</p>
            <p style='font-weight: bold; color: #FFD700;'>IMPORTANT: Pay up to one day before departure.</p>
            """

        contenido += f"""
        <p class='block header'>OFFICE ADDRESS:</p>
        <p style='font-family: Verdana, sans-serif; color: #333;'>Portal Nuevo 270 Plaza Regocijo - Machu Picchu Reservations: <br> 
        <a href='https://maps.app.goo.gl/XcfipVKjbuLeY3no9' style='color: #FF69B4; font-weight: bold;'>👉(Google Maps)👈</a></p>

        <div style='border-left: 4px solid #87CEFA; padding-left: 15px; margin-top: 20px;'>
            <p class='block important'>IMPORTANT:</p>
            <p style='color: #333;'>Please reply to this email with passport photos and your entry date into Peru.</p>
        </div>

        <p class='block header'>DETAILS YOU SHOULD KNOW:</p>
        <ul style='margin-left: 40px; color: #333;'>
            <li>Bus to Machu Picchu ($12) not included; walking option available.</li>
            <li>Breakfast not included; plan meals in Aguas Calientes.</li>
        </ul>

        <p style='color: #333; margin-top: 20px;'>If you have any questions or need assistance, please contact <a href='https://wa.me/51908851429' 
        style='color: #FF69B4; font-weight: bold;'>👉MPR👈</a>. Contact for additional info or options.</p>

        <div style='color: #333; font-size: 12px; margin-top: 20px;'>
            <h2 style='color: #228B22; font-size: 16px;'>MACHUPICCHU RESERVATIONS</h2>
            <p><strong>Schedule:</strong> 7:00-22:00 hrs, Mon-Sat<br><strong>WhatsApp:</strong> <a href='https://api.whatsapp.com/send/?phone=51908851429' style='color: #FF69B4; font-weight: bold;'>👉MPR👈</a></p>
        </div>
        """

        self.mostrar_confirmacion_en_html(contenido)

    def mostrar_confirmacion_en_html(self, contenido):
        nombre_archivo = "confirmacion.html"
        with open(nombre_archivo, "w", encoding="utf-8") as file:
            file.write(f"""
            <html>
            <head>
                <title>Confirmación de Reserva</title>
                <style>
                    body {{ font-family: 'Verdana', sans-serif; margin: 20px; color: #333; }}
                    p {{ line-height: 1.6; font-size: 14px; }}
                    ul {{ list-style-type: none; padding-left: 0; }}
                    ul li::before {{ content: "•"; color: #40E0D0; font-weight: bold; display: inline-block; width: 1em; margin-left: -1em; }}
                    .important {{ font-weight: bold; color: #FF69B4; }}
                    .header {{ font-size: 16px; font-weight: bold; color: #228B22; }}
                </style>
            </head>
            <body>
                {contenido}
            </body>
            </html>
            """)
        print(f"Confirmación guardada como {nombre_archivo}")

class AmazonTour4D:
    def __init__(self, datos):
        self.datos = datos

    def generar_confirmacion(self):
        tour = 'AMAZON TOUR 4D - 3N MANU CULTURAL ZONE'
        tour_dias = 3
        briefing_hora = "6:00 pm"
        primer_nombre = self.datos['nombres'][0].split()[0].capitalize()

        contenido = f"""
        <p style='color: #333;'>Dear {primer_nombre},</p>
        <p style='color: #333;'>Your reservation is confirmed - <span style='color: #2E8B57; font-weight: bold;'>{tour}</span></p>
        
        <table>
            <tr>
                <td style='font-weight: bold; color: #2E8B57;'>START DATE:</td>
                <td style='color: #333;'>{fecha_nombre(self.datos['fecha'][0], self.datos['fecha'][1], self.datos['fecha'][2])}</td>
            </tr>
            <tr>
                <td style='font-weight: bold; color: #2E8B57;'>RETURN DATE:</td>
                <td style='color: #333;'>{fecha_nombre(self.datos['fecha'][0], self.datos['fecha'][1], self.datos['fecha'][2], tour_dias)}</td>
            </tr>
            <tr>
                <td style='font-weight: bold; color: #9ACD32;'>BRIEFING DATE:</td>
                <td style='color: #333;'>{fecha_nombre(self.datos['fecha'][0], self.datos['fecha'][1], self.datos['fecha'][2], -1)}, at {briefing_hora} at Machu Picchu Reservations.</td>
            </tr>
            <tr>
                <td style='font-weight: bold; color: #2E8B57;'>N° PERSON:</td>
                <td style='color: #333;'>{len(self.datos['nombres']):02}</td>
            </tr>
        </table>
        
        <ul style='margin-left: 40px; color: #333;'>
            {''.join([f"<li>{i+1}. {nombre.strip().upper()}</li>" for i, nombre in enumerate(self.datos['nombres'])])}
        </ul>

        <p class='block header'>INCLUDED:</p>
        <ul style='margin-left: 40px;'>
            <li>Ground and river transportation (bus and boat)</li>
            <li>Professional guides equipped with a telescope and binoculars</li>
            <li>Experienced boat driver, crew member, and cook</li>
            <li>Safety equipment</li>
            <li>Breakfasts, lunches, dinners, and snacks</li>
            <li>Accommodation for dietary restrictions (e.g., vegetarian, vegan, gluten-free)</li>
            <li>Rooms with both shared and private bathrooms/showers</li>
            <li>First aid kit</li>
            <li>Rubber boots</li>
            <li>Mineral water at the lodge</li>
        </ul>

        <p class='block header'>DOES NOT INCLUDE:</p>
        <ul style='margin-left: 40px;'>
            <li>Breakfast on the first day</li>
            <li>Alcoholic beverages, soft drinks, and water for the first day’s breakfast</li>
        </ul>

        <p class='block header'>WHAT TO PACK:</p>
        <ul style='margin-left: 40px; color: #333;'>
            <li><strong>Essentials:</strong> Water bottle/canteen, flashlight (with extra batteries), binoculars, camera, extra cash (tips not included).</li>
            <li><strong>Clothing:</strong> Lightweight, breathable long-sleeve shirts and pants (dark colors preferred), rain jacket/poncho, hat, swimwear, towel, sandals, comfortable walking shoes.</li>
            <li><strong>Protection:</strong> Mosquito repellent (minimum 30% DEET), sunscreen.</li>
            <li><strong>Personal:</strong> Personal hygiene items (e.g., toothbrush, toothpaste), personal medications.</li>
            <li><strong>Note:</strong> Pack light for humid rainforest; dark colors reduce insect attraction.</li>
        </ul>

        <p class='block header'>ITINERARY SUMMARY:</p>
        <p style='text-align: center;'><a href='https://www.machupicchureservations.org/tour/amazon-tour-manu-cultural-zone-4-day#itinerary' target='_blank' style='text-decoration: none; color: #2E8B57; font-weight: bold; padding: 8px 16px; border: 2px solid #2E8B57; border-radius: 5px;'>FULL ITINERARY</a></p>
        
        <ul style='margin-left: 40px; color: #333;'>
            <li><strong>Day 01 - Cusco to Cloud Forest:</strong><br>
                  • <span style='color: #3CB371;'>Start:</span> Pick-up 5:30-6:00 AM from Cusco hotel; drive to Ajanaco (3,500m)<br>
                  • <span style='color: #3CB371;'>Travel:</span> Descend through cloud forest<br>
                  • <span style='color: #3CB371;'>Activities:</span> Spot Cock of the Rock, umbrella bird, etc.<br>
                  • <span style='color: #3CB371;'>Stay:</span> Lodge
            </li>
            <li><strong>Day 02 - Atalaya & Machuwasi Lagoon:</strong><br>
                  • <span style='color: #3CB371;'>Start:</span> Breakfast; nature walk for birds/monkeys<br>
                  • <span style='color: #3CB371;'>Travel:</span> 1-hr bus to Atalaya; 30-min boat to lodge<br>
                  • <span style='color: #3CB371;'>Activities:</span> Swim or mud bath; raft on Machuwasi Lagoon (spot shanshos, caimans, etc.); night hike<br>
                  • <span style='color: #3CB371;'>Stay:</span> Lodge with private bathrooms/showers<br>
                  • <span style='color: #3CB371;'>Meals:</span> Breakfast, Lunch, Dinner
            </li>
            <li><strong>Day 03 - Parrot Clay Lick & Ceiba Tree:</strong><br>
                  • <span style='color: #3CB371;'>Start:</span> Dawn boat to parrot clay lick<br>
                  • <span style='color: #3CB371;'>Activities:</span> Breakfast; trail hike to see ceiba tree, monkeys, reptiles; night hike for insects/amphibians<br>
                  • <span style='color: #3CB371;'>Stay:</span> Lodge<br>
                  • <span style='color: #3CB371;'>Meals:</span> Breakfast, Lunch, Dinner
            </li>
            <li><strong>Day 04 - Return to Cusco:</strong><br>
                  • <span style='color: #3CB371;'>Start:</span> Morning trail hike<br>
                  • <span style='color: #3CB371;'>Return:</span> Boat to Atalaya; van to Cusco (5:00-7:00 PM arrival)<br>
                  • <span style='color: #3CB371;'>Activities:</span> Spot hummingbirds, orchids, waterfalls<br>
                  • <span style='color: #3CB371;'>Meals:</span> Breakfast, Lunch
            </li>
        </ul>
        """

        if self.datos['balance'] > 0:
            contenido += f"""
            <p class='block header'>PAYMENT DETAILS:</p>
            <p style='color: #333;'>Outstanding Balance: ${self.datos['balance']}. Pay online via WeTravel (2.9% fee) or in-person at our Cusco office (cash: no fee; card: 3.9% fee) before the trip.</p>
            <p style='font-weight: bold; color: #556B2F;'>IMPORTANT: Pay up to one day before departure.</p>
            """

        contenido += f"""
        <p class='block header'>OFFICE ADDRESS:</p>
        <p style='font-family: Verdana, sans-serif; color: #333;'>Portal Nuevo 270 Plaza Regocijo - Machu Picchu Reservations: <br> 
        <a href='https://maps.app.goo.gl/XcfipVKjbuLeY3no9' style='color: #9ACD32; font-weight: bold;'>👉(Google Maps)👈</a></p>

        <div style='border-left: 4px solid #8FBC8F; padding-left: 15px; margin-top: 20px;'>
            <p class='block important'>IMPORTANT:</p>
            <p style='color: #333;'>Please reply to this email with passport photos and your entry date into Peru.</p>
        </div>

        <p class='block header'>DETAILS YOU SHOULD KNOW:</p>
        <ul style='margin-left: 40px; color: #333;'>
            <li>Rubber boots provided; bring socks and lightweight clothing.</li>
            <li>No breakfast Day 1; plan snacks/drinks for the journey.</li>
        </ul>

        <p style='color: #333; margin-top: 20px;'>If you have any questions or need assistance, please contact <a href='https://wa.me/51908851429' 
        style='color: #9ACD32; font-weight: bold;'>👉MPR👈</a>. Contact for additional info or options.</p>

        <div style='color: #333; font-size: 12px; margin-top: 20px;'>
            <h2 style='color: #2E8B57; font-size: 16px;'>MACHUPICCHU RESERVATIONS</h2>
            <p><strong>Schedule:</strong> 7:00-22:00 hrs, Mon-Sat<br><strong>WhatsApp:</strong> <a href='https://api.whatsapp.com/send/?phone=51908851429' style='color: #9ACD32; font-weight: bold;'>👉MPR👈</a></p>
        </div>
        """

        self.mostrar_confirmacion_en_html(contenido)

    def mostrar_confirmacion_en_html(self, contenido):
        nombre_archivo = "confirmacion.html"
        with open(nombre_archivo, "w", encoding="utf-8") as file:
            file.write(f"""
            <html>
            <head>
                <title>Confirmación de Reserva</title>
                <style>
                    body {{ font-family: 'Verdana', sans-serif; margin: 20px; color: #333; }}
                    p {{ line-height: 1.6; font-size: 14px; }}
                    ul {{ list-style-type: none; padding-left: 0; }}
                    ul li::before {{ content: "•"; color: #3CB371; font-weight: bold; display: inline-block; width: 1em; margin-left: -1em; }}
                    .important {{ font-weight: bold; color: #9ACD32; }}
                    .header {{ font-size: 16px; font-weight: bold; color: #2E8B57; }}
                </style>
            </head>
            <body>
                {contenido}
            </body>
            </html>
            """)
        print(f"Confirmación guardada como {nombre_archivo}")

class AmazonTour3D:
    def __init__(self, datos):
        self.datos = datos

    def generar_confirmacion(self):
        tour = 'AMAZON TOUR 3D – 2N MANU CULTURAL ZONE'
        tour_dias = 2
        briefing_hora = "6:00 pm"
        primer_nombre = self.datos["nombres"][0].split()[0].capitalize()

        contenido = f"""
        <p style='color: #333;'>Dear {primer_nombre},</p>
        <p style='color: #333;'>Your reservation is confirmed - <span style='color: #006400; font-weight: bold;'>{tour}</span></p>
        
        <table>
            <tr>
                <td style='font-weight: bold; color: #006400;'>START DATE:</td>
                <td style='color: #333;'>{fecha_nombre(self.datos['fecha'][0], self.datos['fecha'][1], self.datos['fecha'][2])}</td>
            </tr>
            <tr>
                <td style='font-weight: bold; color: #006400;'>RETURN DATE:</td>
                <td style='color: #333;'>{fecha_nombre(self.datos['fecha'][0], self.datos['fecha'][1], self.datos['fecha'][2], tour_dias)}</td>
            </tr>
            <tr>
                <td style='font-weight: bold; color: #32CD32;'>BRIEFING DATE:</td>
                <td style='color: #333;'>{fecha_nombre(self.datos['fecha'][0], self.datos['fecha'][1], self.datos['fecha'][2], -1)}, at {briefing_hora} at Machu Picchu Reservations.</td>
            </tr>
            <tr>
                <td style='font-weight: bold; color: #006400;'>N° PERSON:</td>
                <td style='color: #333;'>{len(self.datos['nombres']):02}</td>
            </tr>
        </table>
        
        <ul style='margin-left: 40px; color: #333;'>
            {''.join([f"<li>{i+1}. {nombre.strip().upper()}</li>" for i, nombre in enumerate(self.datos['nombres'])])}
        </ul>

        <p class='block header'>INCLUDED:</p>
        <ul style='margin-left: 40px;'>
            <li>Transportation: Includes bus and boat travel for easy navigation.</li>
            <li>Guides: Professional guides with telescope and binoculars for wildlife spotting.</li>
            <li>Crew: Skilled boat operator, crew, and cook provided.</li>
            <li>Safety Gear: All necessary equipment included.</li>
            <li>Meals: Breakfasts, lunches, dinners, and snacks included.</li>
            <li>Dietary Options: Vegetarian, vegan, and gluten-free meals available.</li>
            <li>Accommodation: Lodge with shared and private facilities.</li>
            <li>First Aid: Kit available for emergencies.</li>
            <li>Rubber Boots: Provided for wet or muddy conditions.</li>
            <li>Water: Mineral water supplied at the lodge.</li>
        </ul>

        <p class='block header'>NOT INCLUDED:</p>
        <ul style='margin-left: 40px;'>
            <li>First Breakfast: Not included.</li>
        </ul>

        <p class='block header'>WHAT TO PACK:</p>
        <ul style='margin-left: 40px; color: #333;'>
            <li><strong>Essentials:</strong> Reusable water bottle/canteen, flashlight (with extra batteries), binoculars, camera, extra cash (tips not included).</li>
            <li><strong>Clothing:</strong> Long-sleeve t-shirts (dark colors), long pants (dark colors), rain gear, hat, swimwear, towel, sandals, comfortable walking shoes.</li>
            <li><strong>Protection:</strong> Mosquito repellent (minimum 30% DEET), sunscreen.</li>
            <li><strong>Personal:</strong> Personal hygiene items (e.g., toothbrush, toothpaste).</li>
            <li><strong>Note:</strong> Pack light; dark colors reduce insect attraction.</li>
        </ul>

        <p class='block header'>ITINERARY SUMMARY:</p>
        <p style='text-align: center;'><a href='https://www.machupicchureservations.org/tour/amazon-tour-manu-cultural-zone-3-days#itinerary' target='_blank' style='text-decoration: none; color: #006400; font-weight: bold; padding: 8px 16px; border: 2px solid #006400; border-radius: 5px;'>FULL ITINERARY</a></p>
        
        <ul style='margin-left: 40px; color: #333;'>
            <li><strong>Day 01 - Cusco to Cloud Forest:</strong><br>
                  • <span style='color: #7CFC00;'>Start:</span> Pick-up 5:30-6:00 AM from Cusco hotel; drive to Ajanaco (3,500m)<br>
                  • <span style='color: #7CFC00;'>Travel:</span> Descend through cloud forest (orchids, ferns)<br>
                  • <span style='color: #7CFC00;'>Activities:</span> Spot Andean cock-of-the-rock, trogon, etc.<br>
                  • <span style='color: #7CFC00;'>Stay:</span> Lodge<br>
                  • <span style='color: #7CFC00;'>Meals:</span> Breakfast (en route), Lunch, Dinner
            </li>
            <li><strong>Day 02 - Atalaya & Machuwasi Lagoon:</strong><br>
                  • <span style='color: #7CFC00;'>Start:</span> Breakfast; hike for birds/monkeys<br>
                  • <span style='color: #7CFC00;'>Travel:</span> 1-hr bus to Atalaya; 30-min boat to lodge<br>
                  • <span style='color: #7CFC00;'>Activities:</span> Swim or mud bath; raft on Machuwasi Lagoon (shanshos, caimans); night hike<br>
                  • <span style='color: #7CFC00;'>Stay:</span> Lodge<br>
                  • <span style='color: #7CFC00;'>Meals:</span> Breakfast, Lunch, Dinner
            </li>
            <li><strong>Day 03 - Parrot Clay Lick & Return:</strong><br>
                  • <span style='color: #7CFC00;'>Start:</span> Dawn visit to parrot clay lick<br>
                  • <span style='color: #7CFC00;'>Return:</span> Boat to Atalaya; van to Cusco (arrive 5:00-7:00 PM)<br>
                  • <span style='color: #7CFC00;'>Activities:</span> Spot hummingbirds, waterfalls<br>
                  • <span style='color: #7CFC00;'>Meals:</span> Breakfast, Lunch
            </li>
        </ul>
        """

        if self.datos['balance'] > 0:
            contenido += f"""
            <p class='block header'>PAYMENT DETAILS:</p>
            <p style='color: #333;'>Outstanding Balance: ${self.datos['balance']}. Pay online via WeTravel (2.9% fee) or in-person at our Cusco office (cash: no fee; card: 3.9% fee) before the trip.</p>
            <p style='font-weight: bold; color: #6B8E23;'>IMPORTANT: Pay up to one day before departure.</p>
            """

        contenido += f"""
        <p class='block header'>OFFICE ADDRESS:</p>
        <p style='font-family: Verdana, sans-serif; color: #333;'>Portal Nuevo 270 Plaza Regocijo - Machu Picchu Reservations: <br> 
        <a href='https://maps.app.goo.gl/XcfipVKjbuLeY3no9' style='color: #32CD32; font-weight: bold;'>👉(Google Maps)👈</a></p>

        <div style='border-left: 4px solid #228B22; padding-left: 15px; margin-top: 20px;'>
            <p class='block important'>IMPORTANT:</p>
            <p style='color: #333;'>Please reply to this email with passport photos and your entry date into Peru.</p>
        </div>

        <p class='block header'>DETAILS YOU SHOULD KNOW:</p>
        <ul style='margin-left: 40px; color: #333;'>
            <li>Rubber boots provided; bring socks and lightweight clothing.</li>
            <li>No breakfast Day 1; plan snacks for the journey.</li>
            <li>Notify dietary restrictions at booking.</li>
        </ul>

        <p style='color: #333; margin-top: 20px;'>If you have any questions or need assistance, please contact <a href='https://wa.me/51908851429' 
        style='color: #32CD32; font-weight: bold;'>👉MPR👈</a>. Contact for additional info or options.</p>

        <div style='color: #333; font-size: 12px; margin-top: 20px;'>
            <h2 style='color: #006400; font-size: 16px;'>MACHUPICCHU RESERVATIONS</h2>
            <p><strong>Schedule:</strong> 7:00-22:00 hrs, Mon-Sat<br><strong>WhatsApp:</strong> <a href='https://api.whatsapp.com/send/?phone=51908851429' style='color: #32CD32; font-weight: bold;'>👉MPR👈</a></p>
        </div>
        """

        self.mostrar_confirmacion_en_html(contenido)

    def mostrar_confirmacion_en_html(self, contenido):
        nombre_archivo = "confirmacion.html"
        with open(nombre_archivo, "w", encoding="utf-8") as file:
            file.write(f"""
            <html>
            <head>
                <title>Confirmación de Reserva</title>
                <style>
                    body {{ font-family: 'Verdana', sans-serif; margin: 20px; color: #333; }}
                    p {{ line-height: 1.6; font-size: 14px; }}
                    ul {{ list-style-type: none; padding-left: 0; }}
                    ul li::before {{ content: "•"; color: #7CFC00; font-weight: bold; display: inline-block; width: 1em; margin-left: -1em; }}
                    .important {{ font-weight: bold; color: #32CD32; }}
                    .header {{ font-size: 16px; font-weight: bold; color: #006400; }}
                </style>
            </head>
            <body>
                {contenido}
            </body>
            </html>
            """)
        print(f"Confirmación guardada como {nombre_archivo}")

#TOURS DIARIOS
class RainbowMountainFullDayTour:
    def __init__(self, datos):
        self.datos = datos
        self.hotel = datos.get("hotel", "Please provide your hotel location")

    def generar_confirmacion(self):
        tour = 'RAINBOW MOUNTAIN + RED VALLEY FULL DAY'
        tour_date = fecha_nombre(self.datos['fecha'][0], self.datos['fecha'][1], self.datos['fecha'][2])
        pick_up_time = "4:30 - 5:00 AM"
        primer_nombre = self.datos['nombres'][0].split()[0].capitalize()

        contenido = f"""
        <p style='color: #333;'>Dear {primer_nombre},</p>
        <p style='color: #333;'>Your reservation is confirmed - <span style='color: #008000; font-weight: bold;'>{tour}</span></p>
        
        <table>
            <tr>
                <td style='font-weight: bold; color: #008000;'>DATE TOUR:</td>
                <td style='color: #333;'>{tour_date}</td>
            </tr>
            <tr>
                <td style='font-weight: bold; color: #008000;'>PICK-UP TIME:</td>
                <td style='color: #333;'>{pick_up_time}</td>
            </tr>
            <tr>
                <td style='font-weight: bold; color: #008000;'>HOTEL:</td>
                <td style='color: #333;'>{self.hotel}</td>
            </tr>
            <tr>
                <td style='font-weight: bold; color: #008000;'>N° PERSON:</td>
                <td style='color: #333;'>{len(self.datos['nombres']):02}</td>
            </tr>
        </table>

        <ul style='margin-left: 40px; color: #333;'>
            {''.join([f"<li>{i+1}. {nombre.strip().upper()}</li>" for i, nombre in enumerate(self.datos['nombres'])])}
        </ul>

        <p class='block header'>TOUR INCLUDED:</p>
        <ul style='margin-left: 40px;'>
            <li>Transportation</li>
            <li>Guide</li>
            <li>Breakfast</li>
            <li>Lunch</li>
        </ul>

        <p class='block header'>NOT INCLUDED:</p>
        <ul style='margin-left: 40px;'>
            <li>Entrances = 30 SOLES FOR RAINBOW MOUNTAIN</li>
            <li>Entrances = 20 SOLES FOR RED VALLEY</li>
            <li>Horse</li>
        </ul>

        <p class='block header'>WHAT TO PACK:</p>
        <ul style='margin-left: 40px; color: #333;'>
            <li><strong>Clothing:</strong> Wool hat, t-shirt, layer (e.g., fleece), jacket, long pants, sunglasses, gloves, trekking shoes.</li>
            <li><strong>Essentials:</strong> Small backpack, 2L water (can buy en route), snacks (apples, cereal bars, sweets, chocolate), trekking poles, extra money (Soles).</li>
            <li><strong>Protection:</strong> Sun cream, rain jacket/poncho.</li>
        </ul>

        <p class='block header'>ITINERARY SUMMARY:</p>
        <p style='text-align: center;'><a href='https://www.machupicchureservations.org/tour/rainbow-mountain-full-day-tour#itinerary' target='_blank' style='text-decoration: none; color: #008000; font-weight: bold; padding: 8px 16px; border: 2px solid #008000; border-radius: 5px;'>FULL ITINERARY</a></p>
        
        <ul style='margin-left: 40px; color: #333;'>
            <li><strong>Day 01 - Cusco to Rainbow Mountain & Red Valley:</strong><br>
                  • <span style='color: #90EE90;'>Start:</span> Pick-up 4:30-5:00 AM from hotel or meet at office 5:00 AM; 2-hr drive to Cusipata<br>
                  • <span style='color: #90EE90;'>Activities:</span> Breakfast in Cusipata; 1-hr drive to checkpoint; 1.5-hr hike to Rainbow Mountain (5,100m, 30 Soles entry); 1 hr at summit; optional Red Valley hike (20 Soles entry, 1-1.5 hrs)<br>
                  • <span style='color: #90EE90;'>Return:</span> Lunch in Cusipata (~1:30 PM); 2-hr drive to Cusco (arrive 4:30-5:00 PM)<br>
                  • <span style='color: #90EE90;'>Meals:</span> Breakfast, Lunch<br>
                  • <span style='color: #90EE90;'>Difficulty:</span> Moderate<br>
                  • <span style='color: #90EE90;'>Weather:</span> Cold, windy
            </li>
        </ul>
        """

        if self.datos['balance'] > 0:
            contenido += f"""
            <p class='block header'>PAYMENT DETAILS:</p>
            <p style='color: #333;'>Outstanding Balance: ${self.datos['balance']}. Pay online via WeTravel (2.9% fee) or in-person at our Cusco office (cash: no fee; card: 3.9% fee) before the trip.</p>
            <p style='font-weight: bold; color: #228B22;'>IMPORTANT: Pay up to one day before departure.</p>
            """

        contenido += f"""
        <p class='block header'>OFFICE ADDRESS:</p>
        <p style='font-family: Verdana, sans-serif; color: #333;'>Portal Nuevo 270 Plaza Regocijo - Machu Picchu Reservations: <br> 
        <a href='https://maps.app.goo.gl/XcfipVKjbuLeY3no9' style='color: #00FF00; font-weight: bold;'>👉(Google Maps)👈</a></p>

        <div style='border-left: 4px solid #ADFF2F; padding-left: 15px; margin-top: 20px;'>
            <p class='block important'>IMPORTANT:</p>
            <p style='color: #333;'>Please reply to this email with passport photos and your entry date into Peru.</p>
            <p style='color: #333;'>Confirm by clicking: <a href='https://api.whatsapp.com/send/?phone=51908851429&text=Hello%20MPR!%0A%0A*I%20received%20my%20confirmation%20email%20and%20have%20sent%20my%20passports%20and%20migration%20documents%20to%20the%20email!*%0A%0AMy%20name%20is%20{self.datos['nombres'][0].strip()}.%0AOur%20tour%20is%20{tour}.%0AOur%20tour%20start%20date%20is%20{tour_date}%0A%0A" 
            style='color: #00FF00; font-weight: bold;'>👉(I confirm!)👈</a> via WhatsApp.</p>
        </div>

        <p class='block header'>FREQUENTLY ASKED QUESTIONS:</p>
        <ul style='margin-left: 40px; color: #333;'>
            <li><strong>What is Rainbow Mountain?</strong> Vinicunca, or Montaña de Siete Colores, is a colorful Andean peak (5,100m) known for its unique sedimentary layers.</li>
            <li><strong>How do I get there?</strong> Tours depart from Cusco (3 hrs) or Cusipata; transportation is included.</li>
            <li><strong>How difficult is the trek?</strong> Moderate; 6 km round-trip, 1.5-2 hrs up, high altitude (4,700-5,100m). Acclimatize in Cusco first.</li>
            <li><strong>What should I bring?</strong> Warm layers, sunscreen, water (2L), snacks, trekking gear; see "What to Pack."</li>
            <li><strong>Is it safe?</strong> Yes, with a reputable operator; altitude awareness is key.</li>
            <li><strong>Age restrictions?</strong> No strict limits; suitable for fit travelers; children under 8 need adult supervision.</li>
            <li><strong>Best time to go?</strong> Dry season (May-Sep) for clearer views; weather can vary.</li>
        </ul>

        <p style='color: #333; margin-top: 20px;'>Your contact is <a href='https://api.whatsapp.com/send/?phone=51908851429&text=Hello%20MPR!%0A%0AI%20received%20my%20confirmation%20email.%0A%0AMy%20name%20is%20{self.datos['nombres'][0].strip()}.%0AMy%20tour%20is%20{tour}.%0AMy%20tour%20date%20is%20{tour_date}.%0A%0AI%20have%20the%20following%20questions:%0A%0A1.%0A%0A2.%0A%0A' 
        style='color: #00FF00; font-weight: bold;'>👉MPR👈</a>. Contact for additional info or options.</p>

        <div style='color: #333; font-size: 12px; margin-top: 20px;'>
            <h2 style='color: #008000; font-size: 16px;'>MACHUPICCHU RESERVATIONS</h2>
            <p><strong>Schedule:</strong> 7:00-21:30 hrs, Every Day<br><strong>WhatsApp:</strong> <a href='https://api.whatsapp.com/send/?phone=51908851429' style='color: #00FF00; font-weight: bold;'>👉(MPR)👈</a></p>
        </div>
        """

        self.mostrar_confirmacion_en_html(contenido)

    def mostrar_confirmacion_en_html(self, contenido):
        nombre_archivo = "confirmacion.html"
        with open(nombre_archivo, "w", encoding="utf-8") as file:
            file.write(f"""
            <html>
            <head>
                <title>Confirmación de Reserva</title>
                <style>
                    body {{ font-family: 'Verdana', sans-serif; margin: 20px; color: #333; }}
                    p {{ line-height: 1.6; font-size: 14px; }}
                    ul {{ list-style-type: none; padding-left: 0; }}
                    ul li::before {{ content: "•"; color: #90EE90; font-weight: bold; display: inline-block; width: 1em; margin-left: -1em; }}
                    .important {{ font-weight: bold; color: #00FF00; }}
                    .header {{ font-size: 16px; font-weight: bold; color: #008000; }}
                </style>
            </head>
            <body>
                {contenido}
            </body>
            </html>
            """)
        print(f"Confirmación guardada como {nombre_archivo}")

class HumantayLakeFullDayTour:
    def __init__(self, datos):
        self.datos = datos
        self.hotel = datos.get("hotel", "Please provide your hotel location")

    def generar_confirmacion(self):
        tour = 'HUMANTAY LAKE HIKE FULL DAY'
        tour_date = fecha_nombre(self.datos['fecha'][0], self.datos['fecha'][1], self.datos['fecha'][2])
        pick_up_time = "4:30 - 5:00 AM FROM HOTEL OR 5:00 AM FROM MPR OFFICE"
        primer_nombre = self.datos['nombres'][0].split()[0].capitalize()

        contenido = f"""
        <p style='color: #333;'>Dear {primer_nombre},</p>
        <p style='color: #333;'>Your reservation is confirmed - <span style='color: #008080; font-weight: bold;'>{tour}</span></p>
        
        <table>
            <tr>
                <td style='font-weight: bold; color: #008080;'>DATE TOUR:</td>
                <td style='color: #333;'>{tour_date}</td>
            </tr>
            <tr>
                <td style='font-weight: bold; color: #008080;'>PICK-UP TIME:</td>
                <td style='color: #333;'>{pick_up_time}</td>
            </tr>
            <tr>
                <td style='font-weight: bold; color: #008080;'>HOTEL:</td>
                <td style='color: #333;'>{self.hotel}</td>
            </tr>
            <tr>
                <td style='font-weight: bold; color: #008080;'>N° PERSON:</td>
                <td style='color: #333;'>{len(self.datos['nombres']):02}</td>
            </tr>
        </table>

        <ul style='margin-left: 40px; color: #333;'>
            {''.join([f"<li>{i+1}. {nombre.strip().upper()}</li>" for i, nombre in enumerate(self.datos['nombres'])])}
        </ul>

        <p class='block header'>TOUR INCLUDED:</p>
        <ul style='margin-left: 40px;'>
            <li>Transportation</li>
            <li>Guide</li>
            <li>Breakfast</li>
            <li>Lunch</li>
        </ul>

        <p class='block header'>NOT INCLUDED:</p>
        <ul style='margin-left: 40px;'>
            <li>Entrances = 20 Soles per person</li>
            <li>Horse</li>
        </ul>

        <p class='block header'>WHAT TO PACK:</p>
        <ul style='margin-left: 40px; color: #333;'>
            <li><strong>Clothing:</strong> Wool hat, t-shirt, layer (e.g., fleece), jacket, long pants (lightweight, quick-drying), sunglasses, gloves, trekking shoes, rain jacket/poncho.</li>
            <li><strong>Essentials:</strong> Small backpack, 2L water (can buy en route), snacks (apples, cereal bars, sweets, chocolate), trekking poles, extra money (Soles).</li>
            <li><strong>Protection:</strong> Sun cream.</li>
        </ul>

        <p class='block header'>ITINERARY SUMMARY:</p>
        <p style='text-align: center;'><a href='https://www.machupicchureservations.org/tour/humantay-lake-full-day-tour#itinerary' target='_blank' style='text-decoration: none; color: #008080; font-weight: bold; padding: 8px 16px; border: 2px solid #008080; border-radius: 5px;'>FULL ITINERARY</a></p>
        
        <ul style='margin-left: 40px; color: #333;'>
            <li><strong>Day 01 - Cusco to Humantay Lake & Return:</strong><br>
                  • <span style='color: #98FB98;'>Start:</span> Pick-up 4:30-5:00 AM from hotel or 5:00 AM from MPR office; 2.5-hr drive to Mollepata<br>
                  • <span style='color: #98FB98;'>Activities:</span> Breakfast in Mollepata (7:30-8:30 AM); 1-hr drive to Soraypampa; 1.5-2 hr hike to Humantay Lake (4,200m, 20 Soles entry); 30-min lake visit; 1-hr descent<br>
                  • <span style='color: #98FB98;'>Return:</span> Lunch in Mollepata (2:00-3:00 PM); 2.5-hr drive to Cusco (arrive 5:30-6:00 PM, Plaza Regocijo)<br>
                  • <span style='color: #98FB98;'>Meals:</span> Breakfast, Lunch<br>
                  • <span style='color: #98FB98;'>Difficulty:</span> Moderate<br>
                  • <span style='color: #98FB98;'>Weather:</span> Variable (cold mornings, sunny afternoons)
            </li>
        </ul>
        """

        if self.datos['balance'] > 0:
            contenido += f"""
            <p class='block header'>PAYMENT DETAILS:</p>
            <p style='color: #333;'>Outstanding Balance: ${self.datos['balance']}. Pay online via WeTravel (2.9% fee) or in-person at our Cusco office (cash: no fee; card: 3.9% fee) before the trip.</p>
            <p style='font-weight: bold; color: #2E8B57;'>IMPORTANT: Pay up to one day before departure.</p>
            """

        contenido += f"""
        <p class='block header'>OFFICE ADDRESS:</p>
        <p style='font-family: Verdana, sans-serif; color: #333;'>Portal Nuevo 270 Plaza Regocijo - Machu Picchu Reservations: <br> 
        <a href='https://maps.app.goo.gl/XcfipVKjbuLeY3no9' style='color: #20B2AA; font-weight: bold;'>👉(Google Maps)👈</a></p>

        <div style='border-left: 4px solid #00CED1; padding-left: 15px; margin-top: 20px;'>
            <p class='block important'>IMPORTANT:</p>
            <p style='color: #333;'>Please reply to this email with passport photos and your entry date into Peru.</p>
            <p style='color: #333;'>Confirm by clicking: <a href='https://api.whatsapp.com/send/?phone=51908851429&text=Hello%20MPR!%0A%0A*I%20received%20my%20confirmation%20email%20and%20have%20sent%20my%20passports%20and%20migration%20documents%20to%20the%20email!*%0A%0AMy%20name%20is%20{self.datos['nombres'][0].strip()}.%0AOur%20tour%20is%20{tour}.%0AOur%20tour%20start%20date%20is%20{tour_date}%0A%0A" 
            style='color: #20B2AA; font-weight: bold;'>👉(I confirm!)👈</a> via WhatsApp.</p>
        </div>

        <p class='block header'>FREQUENTLY ASKED QUESTIONS:</p>
        <ul style='margin-left: 40px; color: #333;'>
            <li><strong>What is Humantay Lake?</strong> A turquoise lake at 4,200m in the Andes, near Salkantay Mountain.</li>
            <li><strong>How do I get there?</strong> Tours depart from Cusco (3.5 hrs); transportation included.</li>
            <li><strong>How long is the hike?</strong> 5.5 miles round-trip, 3-4 hrs total.</li>
            <li><strong>Is it difficult?</strong> Moderate; steep inclines, high altitude. Acclimatize in Cusco first.</li>
            <li><strong>Best time to visit?</strong> Dry season (May-Sep) for milder weather.</li>
            <li><strong>Can I swim?</strong> No, it’s a sacred site.</li>
            <li><strong>What to bring?</strong> Layers, water (2L), snacks, sunscreen; see "What to Pack."</li>
            <li><strong>Safety?</strong> Yes, with a guide; altitude precautions needed.</li>
        </ul>

        <p style='color: #333; margin-top: 20px;'>Your contact is <a href='https://api.whatsapp.com/send/?phone=51908851429&text=Hello%20MPR!%0A%0AI%20received%20my%20confirmation%20email.%0A%0AMy%20name%20is%20{self.datos['nombres'][0].strip()}.%0AMy%20tour%20is%20{tour}.%0AMy%20tour%20date%20is%20{tour_date}.%0A%0AI%20have%20the%20following%20questions:%0A%0A1.%0A%0A2.%0A%0A' 
        style='color: #20B2AA; font-weight: bold;'>👉MPR👈</a>. Contact for additional info or options.</p>

        <div style='color: #333; font-size: 12px; margin-top: 20px;'>
            <h2 style='color: #008080; font-size: 16px;'>MACHUPICCHU RESERVATIONS</h2>
            <p><strong>Schedule:</strong> 7:00-21:30 hrs, Every Day<br><strong>WhatsApp:</strong> <a href='https://api.whatsapp.com/send/?phone=51908851429' style='color: #20B2AA; font-weight: bold;'>👉(MPR)👈</a></p>
        </div>
        """

        self.mostrar_confirmacion_en_html(contenido)

    def mostrar_confirmacion_en_html(self, contenido):
        nombre_archivo = "confirmacion.html"
        with open(nombre_archivo, "w", encoding="utf-8") as file:
            file.write(f"""
            <html>
            <head>
                <title>Confirmación de Reserva</title>
                <style>
                    body {{ font-family: 'Verdana', sans-serif; margin: 20px; color: #333; }}
                    p {{ line-height: 1.6; font-size: 14px; }}
                    ul {{ list-style-type: none; padding-left: 0; }}
                    ul li::before {{ content: "•"; color: #98FB98; font-weight: bold; display: inline-block; width: 1em; margin-left: -1em; }}
                    .important {{ font-weight: bold; color: #20B2AA; }}
                    .header {{ font-size: 16px; font-weight: bold; color: #008080; }}
                </style>
            </head>
            <body>
                {contenido}
            </body>
            </html>
            """)
        print(f"Confirmación guardada como {nombre_archivo}")

class PalcoyoFullDayTour:
    def __init__(self, datos):
        self.datos = datos
        self.hotel = datos.get("hotel", "Please provide your hotel location")

    def generar_confirmacion(self):
        tour = 'PALCOYO MOUNTAIN FULL DAY'
        tour_date = fecha_nombre(self.datos['fecha'][0], self.datos['fecha'][1], self.datos['fecha'][2])
        pick_up_time = "4:30 - 5:00 AM (from hotel) or 5:00 AM (from MPR office)"
        primer_nombre = self.datos['nombres'][0].split()[0].capitalize()

        contenido = f"""
        <p style='color: #333;'>Dear {primer_nombre},</p>
        <p style='color: #333;'>Your reservation is confirmed - <span style='color: #3CB371; font-weight: bold;'>{tour}</span></p>
        
        <table>
            <tr>
                <td style='font-weight: bold; color: #3CB371;'>DATE TOUR:</td>
                <td style='color: #333;'>{tour_date}</td>
            </tr>
            <tr>
                <td style='font-weight: bold; color: #3CB371;'>PICK-UP TIME:</td>
                <td style='color: #333;'>{pick_up_time}</td>
            </tr>
            <tr>
                <td style='font-weight: bold; color: #3CB371;'>HOTEL:</td>
                <td style='color: #333;'>{self.hotel}</td>
            </tr>
            <tr>
                <td style='font-weight: bold; color: #3CB371;'>N° PERSON:</td>
                <td style='color: #333;'>{len(self.datos['nombres']):02}</td>
            </tr>
        </table>

        <ul style='margin-left: 40px; color: #333;'>
            {''.join([f"<li>{i+1}. {nombre.strip().upper()}</li>" for i, nombre in enumerate(self.datos['nombres'])])}
        </ul>

        <p class='block header'>TOUR INCLUDED:</p>
        <ul style='margin-left: 40px;'>
            <li>Transportation</li>
            <li>Guide</li>
            <li>Breakfast</li>
            <li>Lunch</li>
        </ul>

        <p class='block header'>NOT INCLUDED:</p>
        <ul style='margin-left: 40px;'>
            <li>Entrance fee: 20 Soles for Palcoyo Mountain (cash payment)</li>
        </ul>

        <p class='block header'>WHAT TO PACK:</p>
        <ul style='margin-left: 40px; color: #333;'>
            <li><strong>Clothing:</strong> Wool hat, t-shirt, layer (fleece/light down jacket), long pants (quick-drying), sunglasses, gloves.</li>
            <li><strong>Essentials:</strong> Small backpack, 2L water, snacks (apples, cereal bars, sweets, chocolate), extra money (Soles).</li>
            <li><strong>Protection:</strong> Sun cream, rain jacket/poncho.</li>
            <li><strong>Optional:</strong> Trekking poles for stability.</li>
        </ul>

        <p class='block header'>ITINERARY SUMMARY:</p>
        <p style='text-align: center;'><a href='https://www.machupicchureservations.org/tour/palcoyo-day-hike-experience#itinerary' target='_blank' style='text-decoration: none; color: #3CB371; font-weight: bold; padding: 8px 16px; border: 2px solid #3CB371; border-radius: 5px;'>FULL ITINERARY</a></p>
        
        <ul style='margin-left: 40px; color: #333;'>
            <li><strong>Day 01 - Cusco to Palcoyo & Return:</strong><br>
                  • <span style='color: #66CDAA;'>Start:</span> Pick-up 4:30-5:00 AM from hotel or 5:00 AM from MPR office; 3.5-hr drive to Palcoyo<br>
                  • <span style='color: #66CDAA;'>Activities:</span> Breakfast in Cusipata; 2-hr guided hike at Palcoyo (20 Soles entry); explore rainbow mountains, stone forest<br>
                  • <span style='color: #66CDAA;'>Return:</span> Lunch in Cusipata; 3.5-hr drive to Cusco (arrive 4:30-5:00 PM)<br>
                  • <span style='color: #66CDAA;'>Meals:</span> Breakfast, Lunch<br>
                  • <span style='color: #66CDAA;'>Difficulty:</span> Easy<br>
                  • <span style='color: #66CDAA;'>Weather:</span> Variable (cool mornings, sunny afternoons)
            </li>
        </ul>
        """

        if self.datos['balance'] > 0:
            contenido += f"""
            <p class='block header'>PAYMENT DETAILS:</p>
            <p style='color: #333;'>Outstanding Balance: ${self.datos['balance']}. Pay online via WeTravel (2.9% fee) or in-person at our Cusco office (cash: no fee; card: 3.9% fee) before the trip.</p>
            <p style='font-weight: bold; color: #2F4F4F;'>IMPORTANT: Pay up to one day before departure.</p>
            """

        contenido += f"""
        <p class='block header'>OFFICE ADDRESS:</p>
        <p style='font-family: Verdana, sans-serif; color: #333;'>Portal Nuevo 270 Plaza Regocijo - Machu Picchu Reservations: <br> 
        <a href='https://maps.app.goo.gl/XcfipVKjbuLeY3no9' style='color: #00FA9A; font-weight: bold;'>👉(Google Maps)👈</a></p>

        <div style='border-left: 4px solid #9ACD32; padding-left: 15px; margin-top: 20px;'>
            <p class='block important'>IMPORTANT:</p>
            <p style='color: #333;'>Please reply to this email with passport photos and your entry date into Peru.</p>
            <p style='color: #333;'>Confirm by clicking: <a href='https://api.whatsapp.com/send/?phone=51908851429&text=Hello%20MPR!%0A%0A*I%20received%20my%20confirmation%20email%20and%20have%20sent%20my%20passports%20and%20migration%20documents%20to%20the%20email!*%0A%0AMy%20name%20is%20{self.datos['nombres'][0].strip()}.%0AOur%20tour%20is%20{tour}.%0AOur%20tour%20start%20date%20is%20{tour_date}%0A%0A" 
            style='color: #00FA9A; font-weight: bold;'>👉(I confirm!)👈</a> via WhatsApp.</p>
        </div>

        <p class='block header'>FREQUENTLY ASKED QUESTIONS:</p>
        <ul style='margin-left: 40px; color: #333;'>
            <li><strong>What is Palcoyo?</strong> A range of three rainbow-colored mountains with vibrant ochre, red, green, blue, and white hues.</li>
            <li><strong>How difficult is the hike?</strong> Easy; 2-hr gentle walk, minimal elevation, suitable for all ages/fitness levels.</li>
            <li><strong>How do I get there?</strong> 3.5-hr drive from Cusco; transportation included.</li>
            <li><strong>What’s the entrance fee?</strong> 20 Soles, payable in cash at the gate.</li>
            <li><strong>Best time to visit?</strong> Dry season (May-Oct) for clear views.</li>
            <li><strong>Palcoyo vs. Vinicunca?</strong> Palcoyo is less crowded, easier, and offers unique stone forests.</li>
            <li><strong>What to bring?</strong> Layers, water (2L), snacks, sunscreen; see "What to Pack."</li>
        </ul>

        <p style='color: #333; margin-top: 20px;'>Your contact is <a href='https://api.whatsapp.com/send/?phone=51908851429&text=Hello%20MPR!%0A%0AI%20received%20my%20confirmation%20email.%0A%0AMy%20name%20is%20{self.datos['nombres'][0].strip()}.%0AMy%20tour%20is%20{tour}.%0AMy%20tour%20date%20is%20{tour_date}.%0A%0AI%20have%20the%20following%20questions:%0A%0A1.%0A%0A2.%0A%0A' 
        style='color: #00FA9A; font-weight: bold;'>👉MPR👈</a>. Contact for additional info or options.</p>

        <div style='color: #333; font-size: 12px; margin-top: 20px;'>
            <h2 style='color: #3CB371; font-size: 16px;'>MACHUPICCHU RESERVATIONS</h2>
            <p><strong>Schedule:</strong> 7:00-21:30 hrs, Every Day<br><strong>WhatsApp:</strong> <a href='https://api.whatsapp.com/send/?phone=51908851429' style='color: #00FA9A; font-weight: bold;'>👉(MPR)👈</a></p>
        </div>
        """

        self.mostrar_confirmacion_en_html(contenido)

    def mostrar_confirmacion_en_html(self, contenido):
        nombre_archivo = "confirmacion.html"
        with open(nombre_archivo, "w", encoding="utf-8") as file:
            file.write(f"""
            <html>
            <head>
                <title>Confirmación de Reserva</title>
                <style>
                    body {{ font-family: 'Verdana', sans-serif; margin: 20px; color: #333; }}
                    p {{ line-height: 1.6; font-size: 14px; }}
                    ul {{ list-style-type: none; padding-left: 0; }}
                    ul li::before {{ content: "•"; color: #66CDAA; font-weight: bold; display: inline-block; width: 1em; margin-left: -1em; }}
                    .important {{ font-weight: bold; color: #00FA9A; }}
                    .header {{ font-size: 16px; font-weight: bold; color: #3CB371; }}
                </style>
            </head>
            <body>
                {contenido}
            </body>
            </html>
            """)
        print(f"Confirmación guardada como {nombre_archivo}")

class ValleSagradoFullDayTour:
    def __init__(self, datos):
        self.datos = datos

    def generar_confirmacion(self):
        tour = 'SACRED VALLEY TOUR FULL DAY'
        tour_date = fecha_nombre(self.datos['fecha'][0], self.datos['fecha'][1], self.datos['fecha'][2])
        pick_up_time = "6:45 AM at Machu Picchu Reservations Office (Portal Nuevo 270, Plaza Regocijo, Cusco)"
        primer_nombre = self.datos['nombres'][0].split()[0].capitalize()

        contenido = f"""
        <p style='color: #333;'>Dear {primer_nombre},</p>
        <p style='color: #333;'>Your reservation is confirmed - <span style='color: #006400; font-weight: bold;'>{tour}</span></p>
        
        <table>
            <tr>
                <td style='font-weight: bold; color: #006400;'>DATE TOUR:</td>
                <td style='color: #333;'>{tour_date}</td>
            </tr>
            <tr>
                <td style='font-weight: bold; color: #006400;'>PICK-UP TIME:</td>
                <td style='color: #333;'>{pick_up_time}</td>
            </tr>
            <tr>
                <td style='font-weight: bold; color: #006400;'>N° PERSON:</td>
                <td style='color: #333;'>{len(self.datos['nombres']):02}</td>
            </tr>
        </table>

        <ul style='margin-left: 40px; color: #333;'>
            {''.join([f"<li>{i+1}. {nombre.strip().upper()}</li>" for i, nombre in enumerate(self.datos['nombres'])])}
        </ul>

        <p class='block header'>TOUR INCLUDED:</p>
        <ul style='margin-left: 40px;'>
            <li>Transportation</li>
            <li>Guide</li>
            <li>Lunch</li>
        </ul>

        <p class='block header'>NOT INCLUDED:</p>
        <ul style='margin-left: 40px;'>
            <li>BTG (70 Soles partial, 130 Soles full)</li>
            <li>Salineras de Maras (20 Soles)</li>
            <li>Breakfast</li>
        </ul>

        <p class='block header'>WHAT TO PACK:</p>
        <ul style='margin-left: 40px; color: #333;'>
            <li><strong>Clothing:</strong> T-shirt, sweater, comfortable pants, waterproof jacket/poncho, comfortable shoes, sunglasses, hat.</li>
            <li><strong>Essentials:</strong> Small backpack, water bottle, snacks, camera, cash (Soles for tickets/purchases).</li>
            <li><strong>Protection:</strong> Sunscreen.</li>
        </ul>

        <p class='block header'>ITINERARY SUMMARY:</p>
        <p style='text-align: center;'><a href='https://www.machupicchureservations.org/tour/sacred-valley-full-day-tour#itinerary' target='_blank' style='text-decoration: none; color: #006400; font-weight: bold; padding: 8px 16px; border: 2px solid #006400; border-radius: 5px;'>FULL ITINERARY</a></p>
        
        <ul style='margin-left: 40px; color: #333;'>
            <li><strong>Day 01 - Cusco to Sacred Valley & Return:</strong><br>
                  • <span style='color: #9ACD32;'>Start:</span> Meet at MPR office 6:45 AM; 45-min drive to Chinchero<br>
                  • <span style='color: #9ACD32;'>Activities:</span> Visit Chinchero (site & weaving), Moray (terraces), Salineras de Maras (salt mines), lunch in Urubamba (~12:30 PM), Ollantaytambo (site, option to stay ~3:00 PM), Pisac (terraces)<br>
                  • <span style='color: #9ACD32;'>Return:</span> Drive to Cusco (arrive 6:30-7:00 PM, Plaza Regocijo)<br>
                  • <span style='color: #9ACD32;'>Meals:</span> Lunch<br>
                  • <span style='color: #9ACD32;'>Duration:</span> ~11-12 hrs
            </li>
        </ul>
        """

        if self.datos['balance'] > 0:
            contenido += f"""
            <p class='block header'>PAYMENT DETAILS:</p>
            <p style='color: #333;'>Outstanding Balance: ${self.datos['balance']}. Pay online via WeTravel (2.9% fee) or in-person at our Cusco office (cash: no fee; card: 3.9% fee) before the trip.</p>
            <p style='font-weight: bold; color: #228B22;'>IMPORTANT: Pay up to one day before departure.</p>
            """

        contenido += f"""
        <p class='block header'>OFFICE ADDRESS:</p>
        <p style='font-family: Verdana, sans-serif; color: #333;'>Portal Nuevo 270 Plaza Regocijo - Machu Picchu Reservations: <br> 
        <a href='https://maps.app.goo.gl/XcfipVKjbuLeY3no9' style='color: #32CD32; font-weight: bold;'>👉(Google Maps)👈</a></p>

        <div style='border-left: 4px solid #556B2F; padding-left: 15px; margin-top: 20px;'>
            <p class='block important'>IMPORTANT:</p>
            <p style='color: #333;'>Please reply to this email with passport photos and your entry date into Peru.</p>
            <p style='color: #333;'>Confirm by clicking: <a href='https://api.whatsapp.com/send/?phone=51908851429&text=Hello%20MPR!%0A%0A*I%20received%20my%20confirmation%20email%20and%20have%20sent%20my%20passports%20and%20migration%20documents%20to%20the%20email!*%0A%0AMy%20name%20is%20{self.datos['nombres'][0].strip()}.%0AOur%20tour%20is%20{tour}.%0AOur%20tour%20start%20date%20is%20{tour_date}%0A%0A" 
            style='color: #32CD32; font-weight: bold;'>👉(I confirm!)👈</a> via WhatsApp.</p>
        </div>

        <p class='block header'>DETAILS YOU SHOULD KNOW:</p>
        <ul style='margin-left: 40px; color: #333;'>
            <li>No hotel pickup; meet at MPR office due to Cusco traffic.</li>
            <li>BTG tickets (70/130 Soles) purchasable at Chinchero; bring cash.</li>
            <li>Option to end in Ollantaytambo (~3:00 PM), skips Pisac.</li>
            <li>No breakfast; pack snacks.</li>
        </ul>

        <p style='color: #333; margin-top: 20px;'>Your contact is <a href='https://api.whatsapp.com/send/?phone=51908851429&text=Hello%20MPR!%0A%0AI%20received%20my%20confirmation%20email.%0A%0AMy%20name%20is%20{self.datos['nombres'][0].strip()}.%0AMy%20tour%20is%20{tour}.%0AMy%20tour%20date%20is%20{tour_date}.%0A%0AI%20have%20the%20following%20questions:%0A%0A1.%0A%0A2.%0A%0A' 
        style='color: #32CD32; font-weight: bold;'>👉MPR👈</a>. Contact for additional info or options.</p>

        <div style='color: #333; font-size: 12px; margin-top: 20px;'>
            <h2 style='color: #006400; font-size: 16px;'>MACHUPICCHU RESERVATIONS</h2>
            <p><strong>Schedule:</strong> 7:00-21:30 hrs, Every Day<br><strong>WhatsApp:</strong> <a href='https://api.whatsapp.com/send/?phone=51908851429' style='color: #32CD32; font-weight: bold;'>👉(MPR)👈</a></p>
        </div>
        """

        self.mostrar_confirmacion_en_html(contenido)

    def mostrar_confirmacion_en_html(self, contenido):
        nombre_archivo = "confirmacion.html"
        with open(nombre_archivo, "w", encoding="utf-8") as file:
            file.write(f"""
            <html>
            <head>
                <title>Confirmación de Reserva</title>
                <style>
                    body {{ font-family: 'Verdana', sans-serif; margin: 20px; color: #333; }}
                    p {{ line-height: 1.6; font-size: 14px; }}
                    ul {{ list-style-type: none; padding-left: 0; }}
                    ul li::before {{ content: "•"; color: #9ACD32; font-weight: bold; display: inline-block; width: 1em; margin-left: -1em; }}
                    .important {{ font-weight: bold; color: #32CD32; }}
                    .header {{ font-size: 16px; font-weight: bold; color: #006400; }}
                </style>
            </head>
            <body>
                {contenido}
            </body>
            </html>
            """)
        print(f"Confirmación guardada como {nombre_archivo}")

class MorayFullDayTour:
    def __init__(self, datos):
        self.datos = datos

    def generar_confirmacion(self):
        tour = 'MORAY + SALT MINES DAY TOUR'
        tour_date = fecha_nombre(self.datos['fecha'][0], self.datos['fecha'][1], self.datos['fecha'][2])
        pick_up_time = "8:45 AM at Machu Picchu Reservations Office (Portal Nuevo 270, Plaza Regocijo, Cusco)"
        primer_nombre = self.datos['nombres'][0].split()[0].capitalize()

        contenido = f"""
        <p style='color: #333;'>Dear {primer_nombre},</p>
        <p style='color: #333;'>Your reservation is confirmed - <span style='color: #8B4513; font-weight: bold;'>{tour}</span></p>
        
        <table>
            <tr>
                <td style='font-weight: bold; color: #8B4513;'>DATE TOUR:</td>
                <td style='color: #333;'>{tour_date}</td>
            </tr>
            <tr>
                <td style='font-weight: bold; color: #8B4513;'>PICK-UP TIME:</td>
                <td style='color: #333;'>{pick_up_time}</td>
            </tr>
            <tr>
                <td style='font-weight: bold; color: #8B4513;'>N° PERSON:</td>
                <td style='color: #333;'>{len(self.datos['nombres']):02}</td>
            </tr>
        </table>

        <ul style='margin-left: 40px; color: #333;'>
            {''.join([f"<li>{i+1}. {nombre.strip().upper()}</li>" for i, nombre in enumerate(self.datos['nombres'])])}
        </ul>

        <p class='block header'>TOUR INCLUDED:</p>
        <ul style='margin-left: 40px;'>
            <li>Professional English-speaking guide</li>
            <li>Transportation</li>
            <li>Group experience with personalized guidance</li>
            <li>Support throughout the tour</li>
            <li>Photo opportunities</li>
        </ul>

        <p class='block header'>NOT INCLUDED:</p>
        <ul style='margin-left: 40px;'>
            <li>Entrance to Maras Salt Mines: 20 Soles (cash)</li>
            <li>Entrance to Moray: 70 Soles (cash, unless you have a BTG)</li>
        </ul>

        <p class='block header'>WHAT TO PACK:</p>
        <ul style='margin-left: 40px; color: #333;'>
            <li><strong>Clothing:</strong> Comfortable layers (e.g., t-shirt, sweater), sturdy shoes/hiking boots.</li>
            <li><strong>Essentials:</strong> Water bottle, snacks, camera/smartphone, cash (Soles for fees/souvenirs), passport.</li>
            <li><strong>Protection:</strong> Sunscreen, sunglasses, hat, light rain jacket/poncho.</li>
        </ul>

        <p class='block header'>ITINERARY SUMMARY:</p>
        <p style='text-align: center;'><a href='https://www.machupicchureservations.org/tour/moray-and-salt-mines-tour#itinerary' target='_blank' style='text-decoration: none; color: #8B4513; font-weight: bold; padding: 8px 16px; border: 2px solid #8B4513; border-radius: 5px;'>FULL ITINERARY</a></p>
        
        <ul style='margin-left: 40px; color: #333;'>
            <li><strong>Day 01 - Cusco to Moray & Maras:</strong><br>
                  • <span style='color: #D2B48C;'>Start:</span> Meet at MPR office 8:45 AM; 1.5-hr drive to Moray<br>
                  • <span style='color: #D2B48C;'>Activities:</span> Guided tour of Moray terraces (70 Soles entry or BTG), free time; drive to Maras Salt Mines, guided tour (20 Soles entry)<br>
                  • <span style='color: #D2B48C;'>Return:</span> 1.5-hr drive to Cusco (arrive ~3:00 PM)<br>
                  • <span style='color: #D2B48C;'>Duration:</span> ~6.5 hrs
            </li>
        </ul>
        """

        if self.datos['balance'] > 0:
            contenido += f"""
            <p class='block header'>PAYMENT DETAILS:</p>
            <p style='color: #333;'>Outstanding Balance: ${self.datos['balance']}. Pay online via WeTravel (2.9% fee) or in-person at our Cusco office (cash: no fee; card: 3.9% fee) before the trip.</p>
            <p style='font-weight: bold; color: #8A2BE2;'>IMPORTANT: Pay up to one day before departure.</p>
            """

        contenido += f"""
        <p class='block header'>OFFICE ADDRESS:</p>
        <p style='font-family: Verdana, sans-serif; color: #333;'>Portal Nuevo 270 Plaza Regocijo - Machu Picchu Reservations: <br> 
        <a href='https://maps.app.goo.gl/XcfipVKjbuLeY3no9' style='color: #CD853F; font-weight: bold;'>👉(Google Maps)👈</a></p>

        <div style='border-left: 4px solid #A0522D; padding-left: 15px; margin-top: 20px;'>
            <p class='block important'>IMPORTANT:</p>
            <p style='color: #333;'>Please reply to this email with passport photos and your entry date into Peru.</p>
            <p style='color: #333;'>Confirm by clicking: <a href='https://api.whatsapp.com/send/?phone=51908851429&text=Hello%20MPR!%0A%0A*I%20received%20my%20confirmation%20email%20and%20have%20sent%20my%20passports%20and%20migration%20documents%20to%20the%20email!*%0A%0AMy%20name%20is%20{self.datos['nombres'][0].strip()}.%0AOur%20tour%20is%20{tour}.%0AOur%20tour%20start%20date%20is%20{tour_date}%0A%0A" 
            style='color: #CD853F; font-weight: bold;'>👉(I confirm!)👈</a> via WhatsApp.</p>
        </div>

        <p class='block header'>DETAILS YOU SHOULD KNOW:</p>
        <ul style='margin-left: 40px; color: #333;'>
            <li>No hotel pickup; meet at MPR office due to traffic.</li>
            <li>Entrance fees (Moray: 70 Soles or BTG; Maras: 20 Soles) payable in cash.</li>
            <li>No meals included; bring snacks/water.</li>
        </ul>

        <p style='color: #333; margin-top: 20px;'>Your contact is <a href='https://api.whatsapp.com/send/?phone=51908851429&text=Hello%20MPR!%0A%0AI%20received%20my%20confirmation%20email.%0A%0AMy%20name%20is%20{self.datos['nombres'][0].strip()}.%0AMy%20tour%20is%20{tour}.%0AMy%20tour%20date%20is%20{tour_date}.%0A%0AI%20have%20the%20following%20questions:%0A%0A1.%0A%0A2.%0A%0A' 
        style='color: #CD853F; font-weight: bold;'>👉MPR👈</a>. Contact for additional info or options.</p>

        <div style='color: #333; font-size: 12px; margin-top: 20px;'>
            <h2 style='color: #8B4513; font-size: 16px;'>MACHUPICCHU RESERVATIONS</h2>
            <p><strong>Schedule:</strong> 7:00-21:30 hrs, Every Day<br><strong>WhatsApp:</strong> <a href='https://api.whatsapp.com/send/?phone=51908851429' style='color: #CD853F; font-weight: bold;'>👉(MPR)👈</a></p>
        </div>
        """

        self.mostrar_confirmacion_en_html(contenido)

    def mostrar_confirmacion_en_html(self, contenido):
        nombre_archivo = "confirmacion.html"
        with open(nombre_archivo, "w", encoding="utf-8") as file:
            file.write(f"""
            <html>
            <head>
                <title>Confirmación de Reserva</title>
                <style>
                    body {{ font-family: 'Verdana', sans-serif; margin: 20px; color: #333; }}
                    p {{ line-height: 1.6; font-size: 14px; }}
                    ul {{ list-style-type: none; padding-left: 0; }}
                    ul li::before {{ content: "•"; color: #D2B48C; font-weight: bold; display: inline-block; width: 1em; margin-left: -1em; }}
                    .important {{ font-weight: bold; color: #CD853F; }}
                    .header {{ font-size: 16px; font-weight: bold; color: #8B4513; }}
                </style>
            </head>
            <body>
                {contenido}
            </body>
            </html>
            """)
        print(f"Confirmación guardada como {nombre_archivo}")

class CuscoCityTour:
    def __init__(self, datos):
        self.datos = datos

    def generar_confirmacion(self):
        tour = 'CUSCO CITY TOUR'
        tour_date = fecha_nombre(self.datos['fecha'][0], self.datos['fecha'][1], self.datos['fecha'][2])
        pick_up_time = "1:00 PM at Machu Picchu Reservations Office (Portal Nuevo 270, Plaza Regocijo, Cusco)"
        primer_nombre = self.datos['nombres'][0].split()[0].capitalize()

        contenido = f"""
        <p style='color: #333;'>Dear {primer_nombre},</p>
        <p style='color: #333;'>Your reservation is confirmed - <span style='color: #800000; font-weight: bold;'>{tour}</span></p>
        
        <table>
            <tr>
                <td style='font-weight: bold; color: #800000;'>DATE TOUR:</td>
                <td style='color: #333;'>{tour_date}</td>
            </tr>
            <tr>
                <td style='font-weight: bold; color: #800000;'>PICK-UP TIME:</td>
                <td style='color: #333;'>{pick_up_time}</td>
            </tr>
            <tr>
                <td style='font-weight: bold; color: #800000;'>N° PERSON:</td>
                <td style='color: #333;'>{len(self.datos['nombres']):02}</td>
            </tr>
        </table>

        <ul style='margin-left: 40px; color: #333;'>
            {''.join([f"<li>{i+1}. {nombre.strip().upper()}</li>" for i, nombre in enumerate(self.datos['nombres'])])}
        </ul>

        <p class='block header'>TOUR INCLUDED:</p>
        <ul style='margin-left: 40px;'>
            <li>Professional English-speaking guide</li>
            <li>Transportation</li>
            <li>Also expert guidance</li>
        </ul>

        <p class='block header'>NOT INCLUDED:</p>
        <ul style='margin-left: 40px;'>
            <li>Entrance to Koricancha: 20 Soles (cash)</li>
            <li>Entrance to Inca ruins (Sacsayhuamán, Qenqo, Pucapucara, Tambomachay): 70 Soles (cash, unless you have a BTG)</li>
        </ul>

        <p class='block header'>WHAT TO PACK:</p>
        <ul style='margin-left: 40px; color: #333;'>
            <li><strong>Clothing:</strong> Comfortable shoes, layered clothing (e.g., t-shirt, sweater).</li>
            <li><strong>Essentials:</strong> Water bottle, camera/smartphone, cash (Soles for fees/souvenirs), passport.</li>
            <li><strong>Protection:</strong> Sunscreen, sunglasses, hat, light rain jacket/poncho.</li>
        </ul>

        <p class='block header'>ITINERARY SUMMARY:</p>
        <p style='text-align: center;'><a href='https://www.machupicchureservations.org/tour/cusco-city-tour#itinerary' target='_blank' style='text-decoration: none; color: #800000; font-weight: bold; padding: 8px 16px; border: 2px solid #800000; border-radius: 5px;'>FULL ITINERARY</a></p>
        
        <ul style='margin-left: 40px; color: #333;'>
            <li><strong>Day 01 - Cusco City Exploration:</strong><br>
                  • <span style='color: #C71585;'>Start:</span> Meet at MPR office 1:00 PM; 10-min walk to Koricancha<br>
                  • <span style='color: #C71585;'>Activities:</span> Guided tour of Koricancha (~1 hr, 20 Soles entry), drive to Sacsayhuamán, Qenqo, Pucapucara, Tambomachay (70 Soles entry or BTG)<br>
                  • <span style='color: #C71585;'>Return:</span> Drive to Cusco (arrive ~6:00 PM, Plaza Regocijo)<br>
                  • <span style='color: #C71585;'>Duration:</span> ~5 hrs
            </li>
        </ul>
        """

        if self.datos['balance'] > 0:
            contenido += f"""
            <p class='block header'>PAYMENT DETAILS:</p>
            <p style='color: #333;'>Outstanding Balance: ${self.datos['balance']}. Pay online via WeTravel (2.9% fee) or in-person at our Cusco office (cash: no fee; card: 3.9% fee) before the trip.</p>
            <p style='font-weight: bold; color: #483D8B;'>IMPORTANT: Pay up to one day before departure.</p>
            """

        contenido += f"""
        <p class='block header'>OFFICE ADDRESS:</p>
        <p style='font-family: Verdana, sans-serif; color: #333;'>Portal Nuevo 270 Plaza Regocijo - Machu Picchu Reservations: <br> 
        <a href='https://maps.app.goo.gl/XcfipVKjbuLeY3no9' style='color: #DAA520; font-weight: bold;'>👉(Google Maps)👈</a></p>

        <div style='border-left: 4px solid #B22222; padding-left: 15px; margin-top: 20px;'>
            <p class='block important'>IMPORTANT:</p>
            <p style='color: #333;'>Please reply to this email with passport photos and your entry date into Peru.</p>
            <p style='color: #333;'>Confirm by clicking: <a href='https://api.whatsapp.com/send/?phone=51908851429&text=Hello%20MPR!%0A%0A*I%20received%20my%20confirmation%20email%20and%20have%20sent%20my%20passports%20and%20migration%20documents%20to%20the%20email!*%0A%0AMy%20name%20is%20{self.datos['nombres'][0].strip()}.%0AOur%20tour%20is%20{tour}.%0AOur%20tour%20start%20date%20is%20{tour_date}%0A%0A" 
            style='color: #DAA520; font-weight: bold;'>👉(I confirm!)👈</a> via WhatsApp.</p>
        </div>

        <p class='block header'>FREQUENTLY ASKED QUESTIONS:</p>
        <ul style='margin-left: 40px; color: #333;'>
            <li><strong>What is the Cusco City Tour?</strong> A half-day tour exploring Koricancha and nearby Inca ruins.</li>
            <li><strong>What’s included?</strong> Guide, transportation; excludes entrance fees.</li>
            <li><strong>How do I book?</strong> Online or at our office by 11:30 AM tour day.</li>
            <li><strong>What to bring?</strong> Passport, layered clothing, water, cash; see "What to Pack."</li>
            <li><strong>Physical requirements?</strong> Moderate walking; suitable for most fitness levels.</li>
            <li><strong>Can I cancel?</strong> Yes, up to 48 hrs before for full refund; fees apply later.</li>
            <li><strong>Weather concerns?</strong> Tours run rain or shine; refunds/rescheduling if cancelled.</li>
        </ul>

        <p style='color: #333; margin-top: 20px;'>Your contact is <a href='https://api.whatsapp.com/send/?phone=51908851429&text=Hello%20MPR!%0A%0AI%20received%20my%20confirmation%20email.%0A%0AMy%20name%20is%20{self.datos['nombres'][0].strip()}.%0AMy%20tour%20is%20{tour}.%0AMy%20tour%20date%20is%20{tour_date}.%0A%0AI%20have%20the%20following%20questions:%0A%0A1.%0A%0A2.%0A%0A' 
        style='color: #DAA520; font-weight: bold;'>👉MPR👈</a>. Contact for additional info or options.</p>

        <div style='color: #333; font-size: 12px; margin-top: 20px;'>
            <h2 style='color: #800000; font-size: 16px;'>MACHUPICCHU RESERVATIONS</h2>
            <p><strong>Schedule:</strong> 7:00-21:30 hrs, Every Day<br><strong>WhatsApp:</strong> <a href='https://api.whatsapp.com/send/?phone=51908851429' style='color: #DAA520; font-weight: bold;'>👉(MPR)👈</a></p>
        </div>
        """

        self.mostrar_confirmacion_en_html(contenido)

    def mostrar_confirmacion_en_html(self, contenido):
        nombre_archivo = "confirmacion.html"
        with open(nombre_archivo, "w", encoding="utf-8") as file:
            file.write(f"""
            <html>
            <head>
                <title>Confirmación de Reserva</title>
                <style>
                    body {{ font-family: 'Verdana', sans-serif; margin: 20px; color: #333; }}
                    p {{ line-height: 1.6; font-size: 14px; }}
                    ul {{ list-style-type: none; padding-left: 0; }}
                    ul li::before {{ content: "•"; color: #C71585; font-weight: bold; display: inline-block; width: 1em; margin-left: -1em; }}
                    .important {{ font-weight: bold; color: #DAA520; }}
                    .header {{ font-size: 16px; font-weight: bold; color: #800000; }}
                </style>
            </head>
            <body>
                {contenido}
            </body>
            </html>
            """)
        print(f"Confirmación guardada como {nombre_archivo}")

class AusangateFullDayTour:
    def __init__(self, datos):
        self.datos = datos
        self.hotel = datos.get("hotel", "Please provide your hotel location")

    def generar_confirmacion(self):
        tour = 'AUSANGATE FULL DAY TOUR – 7 LAKES'
        tour_date = fecha_nombre(self.datos['fecha'][0], self.datos['fecha'][1], self.datos['fecha'][2])
        pick_up_time = "4:30 - 5:00 AM FROM HOTEL or 5:00 AM FROM MPR OFFICE"
        primer_nombre = self.datos['nombres'][0].split()[0].capitalize()

        contenido = f"""
        <p style='color: #333;'>Dear {primer_nombre},</p>
        <p style='color: #333;'>Your reservation is confirmed - <span style='color: #4682B4; font-weight: bold;'>{tour}</span></p>
        
        <table>
            <tr>
                <td style='font-weight: bold; color: #4682B4;'>DATE TOUR:</td>
                <td style='color: #333;'>{tour_date}</td>
            </tr>
            <tr>
                <td style='font-weight: bold; color: #4682B4;'>PICK-UP TIME:</td>
                <td style='color: #333;'>{pick_up_time}</td>
            </tr>
            <tr>
                <td style='font-weight: bold; color: #4682B4;'>HOTEL:</td>
                <td style='color: #333;'>{self.hotel}</td>
            </tr>
            <tr>
                <td style='font-weight: bold; color: #4682B4;'>N° PERSON:</td>
                <td style='color: #333;'>{len(self.datos['nombres']):02}</td>
            </tr>
        </table>

        <ul style='margin-left: 40px; color: #333;'>
            {''.join([f"<li>{i+1}. {nombre.strip().upper()}</li>" for i, nombre in enumerate(self.datos['nombres'])])}
        </ul>

        <p class='block header'>TOUR INCLUDED:</p>
        <ul style='margin-left: 40px;'>
            <li>Round-trip transportation</li>
            <li>Breakfast - Local restaurant</li>
            <li>Lunch - Local restaurant</li>
            <li>Professional English-speaking guide</li>
            <li>First aid kit and oxygen bottle for emergencies</li>
        </ul>

        <p class='block header'>NOT INCLUDED:</p>
        <ul style='margin-left: 40px;'>
            <li>Entrance fee to Ausangate 7 Lakes: 20 Soles (local government fee)</li>
            <li>Hot springs entrance: 10 Soles (cash only)</li>
            <li>Personal gear</li>
            <li>Tips</li>
            <li>Horse</li>
        </ul>

        <p class='block header'>WHAT TO PACK:</p>
        <ul style='margin-left: 40px; color: #333;'>
            <li><strong>Clothing:</strong> Hiking shoes/boots, warm layers (thermal wear, fleece, down jacket), lightweight hiking clothes, waterproof jacket/poncho, hat/cap, sunglasses.</li>
            <li><strong>Essentials:</strong> Water bottle/hydration system, snacks/energy bars, camera/smartphone, extra cash (Soles), small backpack.</li>
            <li><strong>Extras:</strong> Swimsuit, towel (for hot springs), sunscreen.</li>
        </ul>

        <p class='block header'>ITINERARY SUMMARY:</p>
        <p style='text-align: center;'><a href='https://www.machupicchureservations.org/tour/ausangate-7-lakes-full-day-tour#itinerary' target='_blank' style='text-decoration: none; color: #4682B4; font-weight: bold; padding: 8px 16px; border: 2px solid #4682B4; border-radius: 5px;'>FULL ITINERARY</a></p>
        
        <ul style='margin-left: 40px; color: #333;'>
            <li><strong>Day 01 - Cusco to Ausangate 7 Lakes:</strong><br>
                  • <span style='color: #87CEEB;'>Start:</span> Pick-up 4:30-5:00 AM from hotel or 5:00 AM from MPR office; 2-hr drive to Tinki, 1-hr drive to trailhead<br>
                  • <span style='color: #87CEEB;'>Activities:</span> Breakfast, 1.5-hr uphill hike to first lake, explore 7 lakes (20 Soles entry), lunch, hot springs visit (10 Soles entry)<br>
                  • <span style='color: #87CEEB;'>Return:</span> 3-hr drive to Cusco (arrive 7:00-7:30 PM, Plaza Regocijo)<br>
                  • <span style='color: #87CEEB;'>Meals:</span> Breakfast, Lunch<br>
                  • <span style='color: #87CEEB;'>Difficulty:</span> Moderate
            </li>
        </ul>
        """

        if self.datos['balance'] > 0:
            contenido += f"""
            <p class='block header'>PAYMENT DETAILS:</p>
            <p style='color: #333;'>Outstanding Balance: ${self.datos['balance']}. Pay online via WeTravel (2.9% fee) or in-person at our Cusco office (cash: no fee; card: 3.9% fee) before the trip.</p>
            <p style='font-weight: bold; color: #191970;'>IMPORTANT: Pay up to one day before departure.</p>
            """

        contenido += f"""
        <p class='block header'>OFFICE ADDRESS:</p>
        <p style='font-family: Verdana, sans-serif; color: #333;'>Portal Nuevo 270 Plaza Regocijo - Machu Picchu Reservations: <br> 
        <a href='https://maps.app.goo.gl/XcfipVKjbuLeY3no9' style='color: #B0C4DE; font-weight: bold;'>👉(Google Maps)👈</a></p>

        <div style='border-left: 4px solid #708090; padding-left: 15px; margin-top: 20px;'>
            <p class='block important'>IMPORTANT:</p>
            <p style='color: #333;'>Please reply to this email with passport photos and your entry date into Peru.</p>
            <p style='color: #333;'>Confirm by clicking: <a href='https://api.whatsapp.com/send/?phone=51908851429&text=Hello%20MPR!%0A%0A*I%20received%20my%20confirmation%20email%20and%20have%20sent%20my%20passports%20and%20migration%20documents%20to%20the%20email!*%0A%0AMy%20name%20is%20{self.datos['nombres'][0].strip()}.%0AOur%20tour%20is%20{tour}.%0AOur%20tour%20start%20date%20is%20{tour_date}%0A%0A" 
            style='color: #B0C4DE; font-weight: bold;'>👉(I confirm!)👈</a> via WhatsApp.</p>
        </div>

        <p class='block header'>DETAILS YOU SHOULD KNOW:</p>
        <ul style='margin-left: 40px; color: #333;'>
            <li>Entrance fees (7 Lakes: 20 Soles; hot springs: 10 Soles) payable in cash.</li>
            <li>Moderate hike; acclimatize to altitude beforehand.</li>
            <li>Hot springs optional; bring swimsuit if interested.</li>
        </ul>

        <p style='color: #333; margin-top: 20px;'>Your contact is <a href='https://api.whatsapp.com/send/?phone=51908851429&text=Hello%20MPR!%0A%0AI%20received%20my%20confirmation%20email.%0A%0AMy%20name%20is%20{self.datos['nombres'][0].strip()}.%0AMy%20tour%20is%20{tour}.%0AMy%20tour%20date%20is%20{tour_date}.%0A%0AI%20have%20the%20following%20questions:%0A%0A1.%0A%0A2.%0A%0A' 
        style='color: #B0C4DE; font-weight: bold;'>👉MPR👈</a>. Contact for additional info or options.</p>

        <div style='color: #333; font-size: 12px; margin-top: 20px;'>
            <h2 style='color: #4682B4; font-size: 16px;'>MACHUPICCHU RESERVATIONS</h2>
            <p><strong>Schedule:</strong> 7:00-21:30 hrs, Every Day<br><strong>WhatsApp:</strong> <a href='https://api.whatsapp.com/send/?phone=51908851429' style='color: #B0C4DE; font-weight: bold;'>👉(MPR)👈</a></p>
        </div>
        """

        self.mostrar_confirmacion_en_html(contenido)

    def mostrar_confirmacion_en_html(self, contenido):
        nombre_archivo = "confirmacion.html"
        with open(nombre_archivo, "w", encoding="utf-8") as file:
            file.write(f"""
            <html>
            <head>
                <title>Confirmación de Reserva</title>
                <style>
                    body {{ font-family: 'Verdana', sans-serif; margin: 20px; color: #333; }}
                    p {{ line-height: 1.6; font-size: 14px; }}
                    ul {{ list-style-type: none; padding-left: 0; }}
                    ul li::before {{ content: "•"; color: #87CEEB; font-weight: bold; display: inline-block; width: 1em; margin-left: -1em; }}
                    .important {{ font-weight: bold; color: #B0C4DE; }}
                    .header {{ font-size: 16px; font-weight: bold; color: #4682B4; }}
                </style>
            </head>
            <body>
                {contenido}
            </body>
            </html>
            """)
        print(f"Confirmación guardada como {nombre_archivo}")

#CHOQUEQUIRAO
class Choquequirao4Days:
    def __init__(self, datos):
        self.datos = datos

    def generar_confirmacion(self):
        tour = 'CHOQUEQUIRAO TREK 4D-3N'
        tour_dias = 3
        briefing_hora = "6:00 pm"
        primer_nombre = self.datos['nombres'][0].split()[0].capitalize()

        contenido = f"""
        <p style='color: #333;'>Dear {primer_nombre},</p>
        <p style='color: #333;'>Your reservation is confirmed - <span style='color: #4A2F1A; font-weight: bold;'>{tour}</span></p>
        
        <table>
            <tr>
                <td style='font-weight: bold; color: #4A2F1A;'>START DATE:</td>
                <td style='color: #333;'>{fecha_nombre(self.datos['fecha'][0], self.datos['fecha'][1], self.datos['fecha'][2])}</td>
            </tr>
            <tr>
                <td style='font-weight: bold; color: #4A2F1A;'>RETURN DATE:</td>
                <td style='color: #333;'>{fecha_nombre(self.datos['fecha'][0], self.datos['fecha'][1], self.datos['fecha'][2], tour_dias)}</td>
            </tr>
            <tr>
                <td style='font-weight: bold; color: #DEB887;'>BRIEFING DATE:</td>
                <td style='color: #333;'>{fecha_nombre(self.datos['fecha'][0], self.datos['fecha'][1], self.datos['fecha'][2], -1)}, at {briefing_hora} at Machu Picchu Reservations.</td>
            </tr>
            <tr>
                <td style='font-weight: bold; color: #4A2F1A;'>N° PERSON:</td>
                <td style='color: #333;'>{len(self.datos['nombres']):02}</td>
            </tr>
        </table>

        <ul style='margin-left: 40px; color: #333;'>
            {''.join([f"<li>{i+1}. {nombre.strip().upper()}</li>" for i, nombre in enumerate(self.datos['nombres'])])}
        </ul>

        <p class='block header'>TOUR INCLUSIONS:</p>
        <ul style='margin-left: 40px;'>
            <li>Pickup from your hotel</li>
            <li>Professional guide</li>
            <li>Transportation included in the trek</li>
            <li>Choquequirao entrance fees</li>
            <li>Cooks and porters</li>
            <li>Breakfasts, lunches, dinners</li>
            <li>Vegetarian options available</li>
            <li>Potable water available</li>
            <li>Inflatable sleeping pads included</li>
            <li>Dining, kitchen, bathroom tents</li>
            <li>First aid kit</li>
            <li>Free storage in Cusco</li>
        </ul>

        <p class='block header'>WHAT TO PACK:</p>
        <ul style='margin-left: 40px; color: #333;'>
            <li><strong>Clothing:</strong> Moisture-wicking shirts (long/short sleeves), quick-dry hiking pants/shorts, fleece/light down jacket, waterproof/windproof jacket, warm/sun hat, underwear, thermal layers, hiking socks, swimsuit.</li>
            <li><strong>Footwear:</strong> Broken-in hiking boots/shoes, lightweight sandals/flip-flops (camp).</li>
            <li><strong>Essentials:</strong> Daypack (25-35L) with rain cover, water bottles/hydration system (2-3L), headlamp/flashlight (extra batteries), camera/smartphone (charger), dry bags/plastic bags.</li>
            <li><strong>Personal:</strong> Sunscreen, insect repellent, toiletries (toothbrush, toothpaste, wipes), quick-dry towel, biodegradable soap, hand sanitizer, first aid kit, medications.</li>
            <li><strong>Extras:</strong> Snacks (granola bars, nuts, dried fruit, chocolate), trekking poles (optional), gloves.</li>
            <li><strong>Documents:</strong> Passport, travel insurance info, emergency contacts.</li>
        </ul>

        <p class='block header'>ITINERARY SUMMARY:</p>
        <p style='text-align: center;'><a href='https://www.machupicchureservations.org/tour/choquequirao-trek-4-days-2#itinerary' target='_blank' style='text-decoration: none; color: #4A2F1A; font-weight: bold; padding: 8px 16px; border: 2px solid #4A2F1A; border-radius: 5px;'>FULL ITINERARY</a></p>
        
        <ul style='margin-left: 40px; color: #333;'>
            <li><strong>Day 1 - Cusco to Chikiska:</strong><br>
                  • <span style='color: #CD5C5C;'>Start:</span> Pick-up 6:00-6:30 AM from hotel; 3.5-hr drive to Saywite<br>
                  • <span style='color: #CD5C5C;'>Activities:</span> Visit Saywite, 1-hr drive to Capuliyoc, lunch, 3-hr descent to Chikiska<br>
                  • <span style='color: #CD5C5C;'>Stay:</span> Rural lodge (2,900m)<br>
                  • <span style='color: #CD5C5C;'>Meals:</span> Lunch, Dinner
            </li>
            <li><strong>Day 2 - Chikiska to Marampata:</strong><br>
                  • <span style='color: #CD5C5C;'>Start:</span> Breakfast, 1-hr descent to Playa Rosalina (Apurímac River)<br>
                  • <span style='color: #CD5C5C;'>Activities:</span> 3-4 hr steep ascent to Santa Rosa and Marampata, free afternoon<br>
                  • <span style='color: #CD5C5C;'>Stay:</span> Campsite<br>
                  • <span style='color: #CD5C5C;'>Meals:</span> Breakfast, Lunch, Dinner
            </li>
            <li><strong>Day 3 - Marampata to Capuliyoc:</strong><br>
                  • <span style='color: #CD5C5C;'>Start:</span> Breakfast, 2.5-hr descent to river<br>
                  • <span style='color: #CD5C5C;'>Activities:</span> 1-hr ascent to Chikiska, lunch, 3-hr ascent to Capuliyoc<br>
                  • <span style='color: #CD5C5C;'>Stay:</span> Mountain cabins<br>
                  • <span style='color: #CD5C5C;'>Meals:</span> Breakfast, Lunch, Dinner
            </li>
            <li><strong>Day 4 - Capuliyoc to Cusco:</strong><br>
                  • <span style='color: #CD5C5C;'>Start:</span> Breakfast, Pachamama ceremony<br>
                  • <span style='color: #CD5C5C;'>Activities:</span> Lunch, return drive to Cusco (arrive afternoon)<br>
                  • <span style='color: #CD5C5C;'>Meals:</span> Breakfast, Lunch
            </li>
        </ul>
        """

        if self.datos['balance'] > 0:
            contenido += f"""
            <p class='block header'>PAYMENT DETAILS:</p>
            <p style='color: #333;'>Outstanding Balance: ${self.datos['balance']}. Pay online via WeTravel (2.9% fee) or in-person at our Cusco office (cash: no fee; card: 3.9% fee) before the trip.</p>
            <p style='font-weight: bold; color: #FF4500;'>IMPORTANT: Pay up to one day before departure.</p>
            """

        contenido += f"""
        <p class='block header'>OFFICE ADDRESS:</p>
        <p style='font-family: Verdana, sans-serif; color: #333;'>Portal Nuevo 270 Plaza Regocijo - Machu Picchu Reservations: <br> 
        <a href='https://maps.app.goo.gl/XcfipVKjbuLeY3no9' style='color: #DEB887; font-weight: bold;'>👉(Google Maps)👈</a></p>

        <div style='border-left: 4px solid #8B0000; padding-left: 15px; margin-top: 20px;'>
            <p class='block important'>IMPORTANT:</p>
            <p style='color: #333;'>Please reply to this email with passport photos and your entry date into Peru.</p>
        </div>

        <p class='block header'>DETAILS YOU SHOULD KNOW:</p>
        <ul style='margin-left: 40px; color: #333;'>
            <li>Challenging trek; total 62 km, max altitude 3,100m.</li>
            <li>Briefing mandatory at 6:00 PM day before departure.</li>
            <li>Vegetarian options available; notify at booking.</li>
            <li>Pack light; porters carry gear, but personal items needed.</li>
        </ul>

        <p style='color: #333; margin-top: 20px;'>If you have any questions, please contact <a href='https://api.whatsapp.com/send/?phone=51908851429'
        style='color: #DEB887; font-weight: bold;'>👉MPR👈</a>. Contact for additional info or options.</p>

        <div style='color: #333; font-size: 12px; margin-top: 20px;'>
            <h2 style='color: #4A2F1A; font-size: 16px;'>MACHUPICCHU RESERVATIONS</h2>
            <p><strong>Schedule:</strong> 7:00-22:00 hrs, Mon-Sat<br><strong>WhatsApp:</strong> <a href='https://api.whatsapp.com/send/?phone=51908851429' style='color: #DEB887; font-weight: bold;'>👉MPR👈</a></p>
        </div>
        """

        self.mostrar_confirmacion_en_html(contenido)

    def mostrar_confirmacion_en_html(self, contenido):
        nombre_archivo = "confirmacion.html"
        with open(nombre_archivo, "w", encoding="utf-8") as file:
            file.write(f"""
            <html>
            <head>
                <title>Confirmación de Reserva</title>
                <style>
                    body {{ font-family: 'Verdana', sans-serif; margin: 20px; color: #333; }}
                    p {{ line-height: 1.6; font-size: 14px; }}
                    ul {{ list-style-type: none; padding-left: 0; }}
                    ul li::before {{ content: "•"; color: #CD5C5C; font-weight: bold; display: inline-block; width: 1em; margin-left: -1em; }}
                    .important {{ font-weight: bold; color: #DEB887; }}
                    .header {{ font-size: 16px; font-weight: bold; color: #4A2F1A; }}
                </style>
            </head>
            <body>
                {contenido}
            </body>
            </html>
            """)
        print(f"Confirmación guardada como {nombre_archivo}")

class Choquequirao3Days:
    def __init__(self, datos):
        self.datos = datos

    def generar_confirmacion(self):
        tour = 'CHOQUEQUIRAO TREK 3D-2N'
        tour_dias = 2
        briefing_hora = "6:00 pm"
        primer_nombre = self.datos['nombres'][0].split()[0].capitalize()

        contenido = f"""
        <p style="font-family: Verdana, sans-serif; color: #2E8B57;">Dear {primer_nombre},</p>
        <p style="font-family: Verdana, sans-serif; color: #8A2BE2;">Your reservation is confirmed - <span style="font-weight: bold;">{tour}</span></p>
        
        <table style="font-family: Verdana, sans-serif; color: #333;">
            <tr>
                <td style="font-weight: bold; color: #FF6347;">START DATE:</td>
                <td>{fecha_nombre(self.datos['fecha'][0], self.datos['fecha'][1], self.datos['fecha'][2])}</td>
            </tr>
            <tr>
                <td style="font-weight: bold; color: #FF6347;">RETURN DATE:</td>
                <td>{fecha_nombre(self.datos['fecha'][0], self.datos['fecha'][1], self.datos['fecha'][2], tour_dias)}</td>
            </tr>
            <tr>
                <td style="font-weight: bold; color: #20B2AA;">BRIEFING DATE:</td>
                <td>{fecha_nombre(self.datos['fecha'][0], self.datos['fecha'][1], self.datos['fecha'][2], -1)}, at {briefing_hora} at Machu Picchu Reservations.</td>
            </tr>
            <tr>
                <td style="font-weight: bold; color: #FF6347;">N° PERSON:</td>
                <td>{len(self.datos['nombres']):02}</td>
            </tr>
        </table>

        <ul style="margin-left: 40px; font-family: Verdana, sans-serif; color: #333;">
            {''.join([f"<li>{i+1}. {nombre.strip().upper()}</li>" for i, nombre in enumerate(self.datos['nombres'])])}
        </ul>

        <p style="font-family: Verdana, sans-serif; color: #8A2BE2; font-weight: bold;">TOUR INCLUSIONS:</p>
        <ul style="margin-left: 40px; font-family: Verdana, sans-serif; color: #333;">
            <li ">Pickup from your hotel</li>
            <li ">Professional guide</li>
            <li ">Transportation included in the trek</li>
            <li ">Choquequirao entrance fees</li>
            <li ">Cooks and porters</li>
            <li ">Breakfasts, lunches, dinners</li>
            <li ">Vegetarian options available</li>
            <li ">Potable water available</li>
            <li ">Inflatable sleeping pads included</li>
            <li ">Dining, kitchen, bathroom tents</li>
            <li ">First aid kit</li>
            <li ">Free storage in Cusco</li>
        </ul>
        """

        if self.datos['balance'] > 0:
            contenido += f"""
            <p class="block header">Payment Details:</p>
            <p>Outstanding Balance: ${self.datos['balance']}. Pay online via the link in your booking confirmation email (2.9% fee) or in person at our Cusco office during the briefing (cash payments have no extra charge; card payments incur a 3.9% fee).</p>
            <p style="font-weight: bold; color:#ff00fb;">IMPORTANT: We recommend paying the fee up to one day before the briefing.</p>
            """

        # OFICINA, IMPORTANTE, MENSAJE WHATSAPP
        contenido += f"""
            <p class="block header">OFFICE ADDRESS:</p>
            <p style="font-family: Verdana, sans-serif;">Portal Nuevo 270 Plaza Regocijo - Machu Picchu Reservations: <br> 
            Office address link: <a href="https://maps.app.goo.gl/XcfipVKjbuLeY3no9" 
            style="text-decoration: underline; color: #ff0000; font-weight: bold;">👉(Google Maps)👈</a></p>
            
            <div style="border-left: 4px solid #ff6600; padding-left: 15px; margin-top: 20px;">
                <p class="block important" style="font-family: Verdana, sans-serif; font-size: 16px; font-weight: bold; color: #d9534f;">IMPORTANT:</p>
                <p style="font-family: Verdana, sans-serif; color:#333; font-size: 14px;">
                    Please reply to this email by sending your photos of your passports and <strong>inform us of your entry date into the country</strong>. Additionally, <strong>attach the Andean Migration Card</strong> once provided by the Migration Office. These details are essential for <strong>tax and administrative matters (SUNAT)</strong>. 
                </p>
                <p style="font-family: Verdana, sans-serif; color:#333; font-size: 14px;">
                    If you received this email and everything is correct, please let me know by clicking the link below 
                </p>
            </div>
        """

        # REVISAR DATOS
        contenido += f"""
            <div style="border-left: 4px solid #00a20a; padding-left: 15px; margin-top: 20px;">
        """

        contenido += f"""
            <p style="font-weight: bold; color:#007f00; font-size: 14px; font-family: Verdana, Geneva, sans-serif;">
                Additionally, please make sure to update the <strong>WhatsApp numbers</strong> of all participants in your reservation on <strong>We Travel</strong>, or feel free to request assistance with registering them if needed.
            </p>
        </div>
        """
        contenido += f"""
            <p style="font-family: Verdana, sans-serif; color: #333; font-size: 14px; margin-top: 20px;">
                If you have any questions, please contact <a href="https://api.whatsapp.com/send/?phone=51908851429"
                style="color: #8A2BE2; font-weight: bold;">👉MPR👈</a>. Contact for additional info or options.
            <div style="font-family: Verdana, Geneva, sans-serif; padding-top: 10px; margin-top: 20px; color: #333; font-size: 12px;">
                <div style="display: inline-block; vertical-align: top;">
                    <h2 style="color: #000000; margin: 0; font-size: 16px;">MACHUPICCHU RESERVATIONS</h2>
                </div>
            </div>
        """

        self.mostrar_confirmacion_en_html(contenido)

    def mostrar_confirmacion_en_html(self, contenido):
        nombre_archivo = "confirmacion.html"
        with open(nombre_archivo, "w", encoding="utf-8") as file:
            file.write(f"""
            <html>
            <head>
                <title>Confirmación de Reserva</title>
                <style>
                    body {{
                        font-family: 'Verdana', sans-serif;
                        margin: 20px;
                        color: #333;
                    }}
                    p {{
                        line-height: 1.6;
                        font-size: 14px;
                    }}
                    ul {{
                        list-style-type: none;
                        padding-left: 0;
                    }}
                    ul li::before {{
                        content: "•";
                        color: #4CAF50;
                        font-weight: bold;
                        display: inline-block;
                        width: 1em;
                        margin-left: -1em;
                    }}
                    .important {{
                        font-weight: bold;
                        color: #d9534f;
                    }}
                    .header {{
                        font-size: 16px;
                        font-weight: bold;
                        color: #007bff;
                    }}
                    .highlight {{
                        color: #007bff;
                        font-weight: bold;
                    }}
                </style>
            </head>
            <body>
                {contenido}
            </body>
            </html>
            """)

        print(f"Confirmación guardada como {nombre_archivo}")
        
def ajustar_dpi():
    """Ajustar el escalado de DPI para evitar que tkinter se vea grande en pantallas de alta resolución."""
    try:
        ctypes.windll.shcore.SetProcessDpiAwareness(1)  # Windows 8.1 y superior
    except Exception as e:
        try:
            ctypes.windll.user32.SetProcessDPIAware()  # Windows 7 y 8
        except Exception as e:
            pass

def ingresar_datos(tour):
    global ventana, mensajes_whatsapp

    def enviar_datos():
        try:
            # Validación de nombres: convertir a mayúsculas y no pueden contener números
            nombres = [nombre.strip().upper() for nombre in nombres_entry.get().split(',')]  # Convierte a mayúsculas
            for nombre in nombres:
                if any(char.isdigit() for char in nombre):
                    tk.messagebox.showwarning("Error", f"El nombre '{nombre}' no puede contener números.")
                    return
            
            # Validación de la fecha: debe estar en el formato día/mes/año
            try:
                fecha = tuple(map(int, fecha_entry.get().split('/')))  # Convertir a tuple (dia, mes, año)
                if len(fecha) != 3 or not (1 <= fecha[0] <= 31) or not (1 <= fecha[1] <= 12):
                    raise ValueError
            except ValueError:
                tk.messagebox.showwarning("Error", "La fecha no es válida. Asegúrate de usar el formato día/mes/año.")
                return
            
            # Validación del balance: debe ser un número entero
            try:
                balance = int(balance_entry.get())
            except ValueError:
                tk.messagebox.showwarning("Error", "El balance debe ser un número entero.")
                return

            # Si todas las validaciones son correctas, se guarda la información
            datos = {
                "nombres": nombres,
                "fecha": fecha,
                "balance": balance
            }   
        except Exception as e:
            tk.messagebox.showwarning("Error inesperado", f"Ocurrió un error: {str(e)}")
            return
    
        # Conversión de la fecha de inicio del tour
        fecha_inicial = datetime(datos["fecha"][2], datos["fecha"][1], datos["fecha"][0]).date()
        fecha_actual = datetime.now().date()

        # Diccionario de días para cada tour
        tour_dias = {
            Salkantay5DTrain: 4,
            Salkantay4DTrain: 3,
            Salkantay3DTrain: 2,
            Salkantay2D: 1,
            Salkantay5DCar: 4,
            Salkantay4DCar: 3,
            Salkantay3DCar: 2,
            Llactapata3DTrain: 2,
            Llactapata3DCar: 2,
            IncaTrail4D: 3,
            IncaTrail2D: 1,
            IncaTrail1D: 0,
            IncaJungle4DTrain: 3,
            IncaJungle3DTrain: 2,
            IncaJungle4DCar: 3,
            IncaJungle3DCar: 2,
            MachuPicchuFullDay: 0,
            MachuPicchu2DTrain: 1,
            SacredValleyMachuPicchu2D: 1,
            MachuPicchuByCar2D: 1,
            MachuPicchuByCarTrain2D: 1,
            MachuPicchuByCar3D: 2,
            AmazonTour4D: 3,
            AmazonTour3D: 2,
            Choquequirao4Days: 3,
            Choquequirao3Days: 2,
            HumantayLakeFullDayTour: 0,
            RainbowMountainFullDayTour: 0,
            PalcoyoFullDayTour: 0,
            ValleSagradoFullDayTour: 0,
            MorayFullDayTour: 0,
            CuscoCityTour: 0,
            AusangateFullDayTour: 0,
        }

        dias_tour = tour_dias.get(tour, 1)

        # Validaciones de la fecha ingresada
        if fecha_inicial < fecha_actual:
            tk.messagebox.showwarning("Error", "Error, la fecha es incorrecta. No se puede confirmar fechas pasadas. Comuníquese directamente.")
            return
        elif fecha_inicial == fecha_actual and dias_tour > 0:
            tk.messagebox.showwarning("Error", "Este tour no es un Full Day. Para confirmar debe ser mínimo para mañana.")
            return
        
        if "machu_picchu_code" in opciones_tour:
            datos["machu_picchu_code"] = machu_picchu_entry.get().strip() or "0"  # Valor predeterminado "0" si no se ingresa código
        else:
            datos["machu_picchu_code"] = "0"

        if "machu_picchu_code" in opciones_tour:
            machu_picchu_code = machu_picchu_entry.get().strip()

            # Dividir los códigos usando espacio como separador y eliminar espacios adicionales
            machu_picchu_codes = [code.strip() for code in machu_picchu_code.split() if code.strip()]

            # Verificar que al menos se haya ingresado un código
            if len(machu_picchu_codes) < 1:
                tk.messagebox.showwarning("Error", "Debe ingresar al menos 1 código de Machu Picchu.")
                return

            # Convertir las fechas de los códigos
            fechas_codigos = []
            for code in machu_picchu_codes:
                if code == "0":
                    # Si el código es "0", se salta la validación de fechas
                    continue

                if len(code) >= 6:  # Asegurar que el código tenga al menos 6 caracteres
                    codigo_fecha = code[:6]
                    codigo_dia, codigo_mes, codigo_ano = int(codigo_fecha[:2]), int(codigo_fecha[2:4]), int(codigo_fecha[4:6])
                    fecha_codigo = datetime(2000 + codigo_ano, codigo_mes, codigo_dia).date()
                    fechas_codigos.append(fecha_codigo)
                else:
                    tk.messagebox.showwarning("Error", f"El código {code} no tiene el formato correcto.")
                    return

            # Calcular la fecha de ingreso a Machu Picchu dependiendo del tour
            if tour == MachuPicchuByCar3D:
                fecha_ingreso_machu_picchu = fecha_inicial + timedelta(days=1)  # Ingreso el día 2
            else:
                fecha_ingreso_machu_picchu = fecha_inicial + timedelta(days=dias_tour)  # Último día para otros tours

            # Verificación cuando solo hay un código
            if len(machu_picchu_codes) == 1:
                if machu_picchu_codes[0] == "0":
                    # Si el código es "0", no hacemos ninguna validación de fechas y continuamos
                    pass
                else:
                    fecha_codigo = fechas_codigos[0]  # Asegúrate de que hay al menos un código válido en fechas_codigos
                    if tour == MachuPicchuByCar3D:
                        if fecha_codigo != fecha_ingreso_machu_picchu:
                            tk.messagebox.showwarning("Error", f"El código no coincide con la fecha de ingreso a Machu Picchu (día 2).")
                            return
                    elif tour in [IncaTrail4D, IncaTrail2D, IncaTrail1D]:
                        if fecha_codigo != fecha_inicial:
                            tk.messagebox.showwarning("Error", f"El código debe coincidir con la fecha de inicio del tour.")
                            return
                    else:
                        if fecha_codigo != fecha_ingreso_machu_picchu:
                            tk.messagebox.showwarning("Error", "El código no coincide con la fecha de ingreso a Machu Picchu (último día).")
                            return

            # Verificación cuando se ingresan varios códigos
            elif len(machu_picchu_codes) > 1:
                if tour in [IncaTrail4D, IncaTrail2D, IncaTrail1D]:
                    codigo_inicio_valido = False
                    for fecha_codigo in fechas_codigos:
                        if fecha_codigo == fecha_inicial:
                            codigo_inicio_valido = True
                        elif fecha_codigo != fecha_ingreso_machu_picchu:
                            tk.messagebox.showwarning("Error", f"El código {fecha_codigo.strftime('%d/%m/%Y')} no coincide con la fecha de ingreso o de inicio del tour.")
                            return

                    if not codigo_inicio_valido:
                        tk.messagebox.showwarning("Error", "Debe haber al menos un código que coincida con la fecha de inicio del tour.")
                        return

                elif tour == MachuPicchuByCar3D:
                    for fecha_codigo in fechas_codigos:
                        if fecha_codigo != fecha_ingreso_machu_picchu:
                            tk.messagebox.showwarning("Error", f"El código {fecha_codigo.strftime('%d/%m/%Y')} no coincide con la fecha de ingreso a Machu Picchu (día 2).")
                            return
                else:
                    for fecha_codigo in fechas_codigos:
                        if fecha_codigo != fecha_ingreso_machu_picchu:
                            tk.messagebox.showwarning("Error", f"El código {fecha_codigo.strftime('%d/%m/%Y')} no coincide con la fecha de ingreso a Machu Picchu (último día).")
                            return
        if "montaña" in opciones_tour:
            datos["montaña"] = montaña_var.get()

        if "vistadome_ida" in opciones_tour:
            datos["vistadome_ida"] = vistadome_ida_var.get()

        if "vistadome_retorno" in opciones_tour:
            datos["vistadome_retorno"] = vistadome_retorno_var.get()

        if "trekking_poles" in opciones_tour:
            if trekking_poles_entry.get() == "":
                tk.messagebox.showwarning("Error", "Debe completar el campo de bastones de trekking con un número, incluso si es 0.")
                return
            trekking_poles = int(trekking_poles_entry.get())
            if trekking_poles < 0:
                tk.messagebox.showwarning("Error", "El número de bastones de trekking no puede ser menor a 0.")
                return
            if trekking_poles > len(datos["nombres"]):
                tk.messagebox.showwarning("Error", "El número de bastones de trekking no puede exceder el número de pasajeros.")
                return
            datos["trekking_poles"] = trekking_poles

        if "sleeping_bags" in opciones_tour:
            if sleeping_bags_entry.get() == "":
                tk.messagebox.showwarning("Error", "Debe completar el campo de sleeping bags con un número, incluso si es 0.")
                return
            sleeping_bags = int(sleeping_bags_entry.get())
            if sleeping_bags < 0:
                tk.messagebox.showwarning("Error", "El número de sleeping bags no puede ser menor a 0.")
                return
            if sleeping_bags > len(datos["nombres"]):
                tk.messagebox.showwarning("Error", "El número de sleeping bags no puede exceder el número de pasajeros.")
                return
            datos["sleeping_bags"] = sleeping_bags

        if "zipline" in opciones_tour:
            if zipline_entry.get() == "":
                tk.messagebox.showwarning("Error", "Debe completar el campo de Zipline con un número, incluso si es 0.")
                return
            zipline = int(zipline_entry.get())
            if zipline < 0:
                tk.messagebox.showwarning("Error", "El número de participantes para Zipline no puede ser menor a 0.")
                return
            if zipline > len(datos["nombres"]):
                tk.messagebox.showwarning("Error", "El número de participantes para Zipline no puede exceder el número de pasajeros.")
                return
            datos["zipline"] = zipline

        if "hotel" in opciones_tour:
            datos["hotel"] = hotel_var.get() or "Please provide your hotel location. Your hotel should be near the center of Cusco."

        # Teléfono
        phone_number = telefono_entry.get().strip()
        nombre_completo_tour = nombres_tours.get(tour, tour.__name__)
        briefing_date = fecha_inicial - timedelta(days=1)

        if phone_number:
            if re.match(r'^\+\d{10,15}$', phone_number):
                nombre_completo_primer_pax = datos['nombres'][0].strip()
                participantes = '\n'.join([f"- {nombre.strip()}" for nombre in datos['nombres']])

                # Generación de mensajes
                if dias_tour > 0:
                    briefing_hora = "6:00 pm"
                    if tour in [Salkantay5DTrain, Salkantay5DCar, Salkantay4DTrain, Salkantay4DCar, Salkantay3DTrain, Salkantay3DCar, Salkantay2D, Llactapata3DTrain, Llactapata3DCar]:
                        briefing_hora = "7:00 pm"
                        message = (
                            f"*Hello {nombre_completo_primer_pax}, your reservation for {nombre_completo_tour} has been confirmed!*\n\n"
                            f"Dates: {fecha_nombre(*datos['fecha'])} to {fecha_nombre(datos['fecha'][0], datos['fecha'][1], datos['fecha'][2], dias_tour)}\n"
                            f"*IMPORTANT: Briefing on {briefing_date.strftime('%A, %d %B %Y')}, at {briefing_hora} at office Machu Picchu Reservations.*\n"
                            f"Participants:\n{participantes}\n"
                            "An email has been sent with the tickets and reservation details.\n"
                            "_Thank you for trusting us!_\n"
                        )
                    if tour in [MachuPicchuFullDay, MachuPicchu2DTrain, MachuPicchuByCar2D, MachuPicchuByCarTrain2D, MachuPicchuByCar3D]:
                        message = (
                            f"*Hello {nombre_completo_primer_pax}, your reservation for {nombre_completo_tour} has been confirmed!*\n\n"
                            f"Dates: {fecha_nombre(*datos['fecha'])} to {fecha_nombre(datos['fecha'][0], datos['fecha'][1], datos['fecha'][2], dias_tour)}\n"
                            f"*IMPORTANT: Briefing on {briefing_date.strftime('%A, %d %B %Y')}, at office Machu Picchu Reservations office.*\n"
                            f"You must come to the office between 7:00 am and 10:00 pm to pick up all your tickets."
                            f"Participants:\n{participantes}\n"
                            "An email has been sent with the tickets and reservation details.\n"
                            "_Thank you for trusting us!_\n"
                        )
                else:
                    if tour in [IncaTrail1D]:
                        briefing_hora = "6:00 pm"
                        message = (
                            f"*Hello {nombre_completo_primer_pax}, your reservation for {nombre_completo_tour} has been confirmed!*\n\n"
                            f"Tour Date: {fecha_nombre(*datos['fecha'])}\n"
                            f"*IMPORTANT: Briefing on {briefing_date.strftime('%A, %d %B %Y')}, at {briefing_hora} at office Machu Picchu Reservations.*\n"
                            f"Participants:\n{participantes}\n"
                            "An email has been sent with the reservation details.\n"
                            "_Thank you for trusting us!_\n"
                        )
                    elif tour in [ValleSagradoFullDayTour, MorayFullDayTour, CuscoCityTour, ]:
                        message = (
                            f"*Hello {nombre_completo_primer_pax}, your reservation for {nombre_completo_tour} has been confirmed!*\n\n"
                            f"Tour Date: {fecha_nombre(*datos['fecha'])}\n"
                            f"Pick up location: Machu Picchu Reservations office\n"
                            f"Participants:\n{participantes}\n"
                            "An email has been sent with the reservation details.\n"
                            "_Thank you for trusting us!_\n"
                        )
                    else:
                        message = (
                            f"*Hello {nombre_completo_primer_pax}, your reservation for {nombre_completo_tour} has been confirmed!*\n\n"
                            f"Tour Date: {fecha_nombre(*datos['fecha'])}\n"
                            f"Pick up location: from your hotel or from the Machu Picchu Reservations office\n"
                            f"Participants:\n{participantes}\n"
                            "An email has been sent with the reservation details.\n"
                            "_Thank you for trusting us!_\n"
                        )

                mensajes_whatsapp.append((phone_number, message))
            else:
                tk.messagebox.showwarning("Error", "Por favor, ingrese un número de teléfono válido con código de país.")
                return
        else:
            print("Número de teléfono no proporcionado, omitiendo envío de WhatsApp.")

        # Llamar a la función que ejecuta la consola con los datos del tour
        ejecutar_en_consola_con_datos(tour, datos)

    limpiar_ventana(ventana)

    if tour == Salkantay5DTrain:
        tk.Label(ventana, text="SALKANTAY 5D BY TRAIN").pack(pady=5)
        
    elif tour == Salkantay4DTrain:
        tk.Label(ventana, text="SALKANTAY 4D BY TRAIN").pack(pady=5)
        
    elif tour == Salkantay3DTrain:
        tk.Label(ventana, text="SALKANTAY 3D BY TRAIN").pack(pady=5)
        
    elif tour == Llactapata3DTrain:
        tk.Label(ventana, text="LLACTAPATA BY TRAIN").pack(pady=5)
        
    elif tour == IncaTrail4D:
        tk.Label(ventana, text="INCA TRIAL 4D").pack(pady=5)
        
    elif tour == IncaTrail2D:
        tk.Label(ventana, text="INCA TRAIL 2D").pack(pady=5)
        
    elif tour == IncaTrail1D:
        tk.Label(ventana, text="INCA TRAIL 1D").pack(pady=5)

    elif tour == Salkantay5DCar:
        tk.Label(ventana, text="SALKANTAY 5D BY CAR").pack(pady=5)
        
    elif tour == Salkantay4DCar:
        tk.Label(ventana, text="SALKANTAY 4D BY CAR").pack(pady=5)
        
    elif tour == Salkantay3DCar:
        tk.Label(ventana, text="SALKANTAY 3D BY CAR").pack(pady=5)
        
    elif tour == Llactapata3DCar:
        tk.Label(ventana, text="LLACTAPATA CAR").pack(pady=5)
        
    elif tour == Salkantay2D:
        tk.Label(ventana, text="SALKANTAY 2D").pack(pady=5)
        
    elif tour == IncaJungle4DTrain:
        tk.Label(ventana, text="INCA JUNGLE 4D BY TRAIN").pack(pady=5)
        
    elif tour == IncaJungle3DTrain:
        tk.Label(ventana, text="INCA JUNGLE 3D BY TRAIN").pack(pady=5)
        
    elif tour == IncaJungle4DCar:
        tk.Label(ventana, text="INCA JUNGLE 4D BY CAR").pack(pady=5)
        
    elif tour == IncaJungle3DCar:
        tk.Label(ventana, text="INCA JUNGLE 3D BY CAR").pack(pady=5)
        
    elif tour == MachuPicchuByCar2D:
        tk.Label(ventana, text="MAPI BY CAR 2D").pack(pady=5)
        
    elif tour == MachuPicchuByCarTrain2D:
        tk.Label(ventana, text="MAPI BY CAR Y BY TRAIN 2D").pack(pady=5)
        
    elif tour == MachuPicchuFullDay:
        tk.Label(ventana, text="MAPI FULL DAY").pack(pady=5)
        
    elif tour == MachuPicchu2DTrain:
        tk.Label(ventana, text="MAPI BY TRAIN 2D").pack(pady=5)
        
    elif tour == SacredValleyMachuPicchu2D:
        tk.Label(ventana, text="SACRED VALLEY + MAPI").pack(pady=5)
        
    elif tour == MachuPicchuByCar3D:
        tk.Label(ventana, text="MAPI BY CAR 3D").pack(pady=5)

    elif tour == CuscoCitySacredValleyMachuPicchu3D:
        tk.Label(ventana, text="CITY + VALLE- MAPI 3D").pack(pady=5)
        tk.Label(ventana, text="Este tour solo se aplica a reservas privadas", fg="red").pack()
        
    elif tour == AmazonTour4D:
        tk.Label(ventana, text="AMAZON MANU 4D").pack(pady=5)
        
    elif tour == AmazonTour3D:
        tk.Label(ventana, text="AMAZON MANU 3D").pack(pady=5)
        
    elif tour == Choquequirao4Days:
        tk.Label(ventana, text="CHOQUEQUIRAO 4D").pack(pady=5)
        
    elif tour == Choquequirao3Days:
        tk.Label(ventana, text="CHOQUERIRAO 3D").pack(pady=5)
        
    elif tour == HumantayLakeFullDayTour:
        tk.Label(ventana, text="HUMANTAY").pack(pady=5)
        
    elif tour == RainbowMountainFullDayTour:
        tk.Label(ventana, text="RAINBOW MOUNTAIN").pack(pady=5)
        
    elif tour == PalcoyoFullDayTour:
        tk.Label(ventana, text="PALCOYO FULL DAY").pack(pady=5)
        
    elif tour == ValleSagradoFullDayTour:
        tk.Label(ventana, text="VALLE SAGRADO").pack(pady=5)

    elif tour == MorayFullDayTour:
        tk.Label(ventana, text="MORAY FULL DAY").pack(pady=5)

    elif tour == CuscoCityTour:
        tk.Label(ventana, text="CUSCO CITY TOUR").pack(pady=5)

    elif tour == AusangateFullDayTour:
        tk.Label(ventana, text="AUSANGATE FULL DAY - 7 LAKES").pack(pady=5)

    tk.Label(ventana, text="Nombres (separados por comas):").pack(pady=5)
    nombres_entry = tk.Entry(ventana)
    nombres_entry.pack()

    tk.Label(ventana, text="Fecha (dia/mes/año):").pack(pady=5)
    fecha_entry = tk.Entry(ventana)
    fecha_entry.pack()

    tk.Label(ventana, text="Saldo:").pack(pady=5)
    balance_entry = tk.Entry(ventana)
    balance_entry.pack()

    opciones_tour = []

    if tour in [Salkantay5DTrain, Salkantay4DTrain]:
        opciones_tour = ["machu_picchu_code", "montaña", "vistadome_retorno", "trekking_poles", "sleeping_bags", "zipline"]

        tk.Label(ventana, text="Códigos Machupicchu:").pack(pady=5)
        machu_picchu_entry = tk.Entry(ventana)
        machu_picchu_entry.pack()

        tk.Label(ventana, text="Montaña:").pack(pady=5)
        montaña_var = tk.StringVar(value="0")

        ttk.Radiobutton(ventana, text="Wayna Picchu Mountain", variable=montaña_var, value="WAYNA PICCHU MOUNTAIN").pack()
        ttk.Radiobutton(ventana, text="Machu Picchu Mountain", variable=montaña_var, value="MACHU PICCHU MOUNTAIN").pack()

        tk.Label(ventana, text="Vistadome en el retorno:").pack(pady=5)
        vistadome_retorno_var = tk.BooleanVar()
        ttk.Checkbutton(ventana, text="Sí", variable=vistadome_retorno_var).pack()

        frame_horizontal = tk.Frame(ventana)
        frame_horizontal.pack(pady=10)

        opciones_adicionales = {
            "TP": "Trekking Poles",
            "SB": "Sleeping Bags",
            "ZIP": "Zipline"
        }

        for codigo, descripcion in opciones_adicionales.items():
            contenedor = tk.Frame(frame_horizontal)
            contenedor.pack(side=tk.LEFT, padx=10)

            etiqueta = tk.Label(contenedor, text=codigo, font=("Verdana", 9))
            etiqueta.pack()

            entrada = tk.Entry(contenedor, width=5, justify='center')
            entrada.pack(pady=5)

            if codigo == "TP":
                trekking_poles_entry = entrada
            elif codigo == "SB":
                sleeping_bags_entry = entrada
            elif codigo == "ZIP":
                zipline_entry = entrada
    
    elif tour in [Salkantay3DTrain, Llactapata3DTrain, IncaTrail4D, IncaTrail2D]:
        opciones_tour = ["machu_picchu_code", "montaña", "vistadome_retorno", "trekking_poles", "sleeping_bags"]

        tk.Label(ventana, text="Códigos Machupicchu:").pack(pady=5)
        machu_picchu_entry = tk.Entry(ventana)
        machu_picchu_entry.pack()

        tk.Label(ventana, text="Montaña:").pack(pady=5)
        montaña_var = tk.StringVar(value="0")

        ttk.Radiobutton(ventana, text="Wayna Picchu Mountain", variable=montaña_var, value="WAYNA PICCHU MOUNTAIN").pack()
        ttk.Radiobutton(ventana, text="Machu Picchu Mountain", variable=montaña_var, value="MACHU PICCHU MOUNTAIN").pack()

        tk.Label(ventana, text="Vistadome en el retorno:").pack(pady=5)
        vistadome_retorno_var = tk.BooleanVar()
        ttk.Checkbutton(ventana, text="Sí", variable=vistadome_retorno_var).pack()

        frame_horizontal = tk.Frame(ventana)
        frame_horizontal.pack(pady=10)

        opciones_adicionales = {
            "TP": "Trekking Poles",
            "SB": "Sleeping Bags"
        }

        for codigo, descripcion in opciones_adicionales.items():
            contenedor = tk.Frame(frame_horizontal)
            contenedor.pack(side=tk.LEFT, padx=10)

            etiqueta = tk.Label(contenedor, text=codigo, font=("Verdana", 9))
            etiqueta.pack()

            entrada = tk.Entry(contenedor, width=5, justify='center')
            entrada.pack(pady=5)

            if codigo == "TP":
                trekking_poles_entry = entrada
            elif codigo == "SB":
                sleeping_bags_entry = entrada

    elif tour in [IncaTrail1D]:
        opciones_tour = ["machu_picchu_code", "montaña", "vistadome_retorno", "trekking_poles"]

        tk.Label(ventana, text="Códigos Machupicchu:").pack(pady=5)
        machu_picchu_entry = tk.Entry(ventana)
        machu_picchu_entry.pack()

        tk.Label(ventana, text="Montaña:").pack(pady=5)
        montaña_var = tk.StringVar(value="0")

        ttk.Radiobutton(ventana, text="Wayna Picchu Mountain", variable=montaña_var, value="WAYNA PICCHU MOUNTAIN").pack()
        ttk.Radiobutton(ventana, text="Machu Picchu Mountain", variable=montaña_var, value="MACHU PICCHU MOUNTAIN").pack()

        tk.Label(ventana, text="Vistadome en el retorno:").pack(pady=5)
        vistadome_retorno_var = tk.BooleanVar()
        ttk.Checkbutton(ventana, text="Sí", variable=vistadome_retorno_var).pack()

        frame_horizontal = tk.Frame(ventana)
        frame_horizontal.pack(pady=10)

        opciones_adicionales = {
            "TP": "Trekking Poles",
        }

        for codigo, descripcion in opciones_adicionales.items():
            contenedor = tk.Frame(frame_horizontal)
            contenedor.pack(side=tk.LEFT, padx=10)

            etiqueta = tk.Label(contenedor, text=codigo, font=("Verdana", 9))
            etiqueta.pack()

            entrada = tk.Entry(contenedor, width=5, justify='center')
            entrada.pack(pady=5)

            if codigo == "TP":
                trekking_poles_entry = entrada

    elif tour in [Salkantay5DCar, Salkantay4DCar]:
        opciones_tour = ["machu_picchu_code", "trekking_poles", "sleeping_bags", "zipline"]

        tk.Label(ventana, text="Códigos Machupicchu:").pack(pady=5)
        machu_picchu_entry = tk.Entry(ventana)
        machu_picchu_entry.pack()

        frame_horizontal = tk.Frame(ventana)
        frame_horizontal.pack(pady=10)

        opciones_adicionales = {
            "TP": "Trekking Poles",
            "SB": "Sleeping Bags",
            "ZIP": "Zipline"
        }

        for codigo, descripcion in opciones_adicionales.items():
            contenedor = tk.Frame(frame_horizontal)
            contenedor.pack(side=tk.LEFT, padx=10)

            etiqueta = tk.Label(contenedor, text=codigo, font=("Verdana", 9))
            etiqueta.pack()

            entrada = tk.Entry(contenedor, width=5, justify='center')
            entrada.pack(pady=5)

            if codigo == "TP":
                trekking_poles_entry = entrada
            elif codigo == "SB":
                sleeping_bags_entry = entrada
            elif codigo == "ZIP":
                zipline_entry = entrada

    elif tour in [Salkantay3DCar, Llactapata3DCar]:
        opciones_tour = ["machu_picchu_code", "trekking_poles", "sleeping_bags"]

        tk.Label(ventana, text="Códigos Machupicchu:").pack(pady=5)
        machu_picchu_entry = tk.Entry(ventana)
        machu_picchu_entry.pack()

        frame_horizontal = tk.Frame(ventana)
        frame_horizontal.pack(pady=10)

        opciones_adicionales = {
            "TP": "Trekking Poles",
            "SB": "Sleeping Bags"
        }

        for codigo, descripcion in opciones_adicionales.items():
            contenedor = tk.Frame(frame_horizontal)
            contenedor.pack(side=tk.LEFT, padx=10)

            etiqueta = tk.Label(contenedor, text=codigo, font=("Verdana", 9))
            etiqueta.pack()

            entrada = tk.Entry(contenedor, width=5, justify='center')
            entrada.pack(pady=5)

            if codigo == "TP":
                trekking_poles_entry = entrada
            elif codigo == "SB":
                sleeping_bags_entry = entrada

    elif tour == Salkantay2D:
        opciones_tour = ["trekking_poles", "sleeping_bags"]

        frame_horizontal = tk.Frame(ventana)
        frame_horizontal.pack(pady=10)

        opciones_adicionales = {
            "TP": "Trekking Poles",
            "SB": "Sleeping Bags"
        }

        for codigo, descripcion in opciones_adicionales.items():
            contenedor = tk.Frame(frame_horizontal)
            contenedor.pack(side=tk.LEFT, padx=10)

            etiqueta = tk.Label(contenedor, text=codigo, font=("Verdana", 9))
            etiqueta.pack()

            entrada = tk.Entry(contenedor, width=5, justify='center')
            entrada.pack(pady=5)

            if codigo == "TP":
                trekking_poles_entry = entrada
            elif codigo == "SB":
                sleeping_bags_entry = entrada
        
    elif tour == IncaJungle4DTrain or tour == IncaJungle3DTrain:
        opciones_tour = ["machu_picchu_code", "montaña", "vistadome_retorno"]
        tk.Label(ventana, text="Códigos Machupicchu:").pack(pady=5)
        machu_picchu_entry = tk.Entry(ventana)
        machu_picchu_entry.pack()

        tk.Label(ventana, text="Montaña:").pack(pady=5)
        montaña_var = tk.StringVar(value="0")

        ttk.Radiobutton(ventana, text="Wayna Picchu Mountain", variable=montaña_var, value="WAYNA PICCHU MOUNTAIN").pack()
        ttk.Radiobutton(ventana, text="Machu Picchu Mountain", variable=montaña_var, value="MACHU PICCHU MOUNTAIN").pack()

        tk.Label(ventana, text="Vistadome en el retorno:").pack(pady=5)
        vistadome_retorno_var = tk.BooleanVar()
        ttk.Checkbutton(ventana, text="Sí", variable=vistadome_retorno_var).pack()

    elif tour == IncaJungle4DCar or tour == IncaJungle3DCar or tour == MachuPicchuByCar2D:
        opciones_tour = ["machu_picchu_code"]
        tk.Label(ventana, text="Códigos Machupicchu:").pack(pady=5)
        machu_picchu_entry = tk.Entry(ventana)
        machu_picchu_entry.pack()

    elif tour == MachuPicchuByCarTrain2D:
        opciones_tour = ["machu_picchu_code", "vistadome_retorno", "montaña"]

        tk.Label(ventana, text="Códigos Machupicchu:").pack(pady=5)
        machu_picchu_entry = tk.Entry(ventana)
        machu_picchu_entry.pack()

        tk.Label(ventana, text="Montaña:").pack(pady=5)
        montaña_var = tk.StringVar(value="0")

        ttk.Radiobutton(ventana, text="Wayna Picchu Mountain", variable=montaña_var, value="WAYNA PICCHU MOUNTAIN").pack()
        ttk.Radiobutton(ventana, text="Machu Picchu Mountain", variable=montaña_var, value="MACHU PICCHU MOUNTAIN").pack()

        tk.Label(ventana, text="Vistadome en el retorno:").pack(pady=5)
        vistadome_retorno_var = tk.BooleanVar()
        ttk.Checkbutton(ventana, text="Sí", variable=vistadome_retorno_var).pack()

    elif tour in [MachuPicchuFullDay, MachuPicchu2DTrain, SacredValleyMachuPicchu2D, CuscoCitySacredValleyMachuPicchu3D]:
        opciones_tour = ["machu_picchu_code", "montaña", "vistadome_ida", "vistadome_retorno"]

        tk.Label(ventana, text="Códigos Machupicchu:").pack(pady=5)
        machu_picchu_entry = tk.Entry(ventana)
        machu_picchu_entry.pack()

        tk.Label(ventana, text="Montaña:").pack(pady=5)
        montaña_var = tk.StringVar(value="0")

        ttk.Radiobutton(ventana, text="Wayna Picchu Mountain", variable=montaña_var, value="WAYNA PICCHU MOUNTAIN").pack()
        ttk.Radiobutton(ventana, text="Machu Picchu Mountain", variable=montaña_var, value="MACHU PICCHU MOUNTAIN").pack()

        tk.Label(ventana, text="Opciones Vistadome:").pack()
        frame_horizontal = tk.Frame(ventana)
        frame_horizontal.pack(pady=10)

        opciones_vistadome = {
            "IDA": "Vistadome ida",
            "RET": "Vistadome retorno"
        }

        for codigo, descripcion in opciones_vistadome.items():
            contenedor = tk.Frame(frame_horizontal)
            contenedor.pack(side=tk.LEFT, padx=10)

            etiqueta = tk.Label(contenedor, text=codigo, font=("Verdana", 9))
            etiqueta.pack()

            checkbox_var = tk.BooleanVar()
            ttk.Checkbutton(contenedor, text="Sí", variable=checkbox_var).pack(pady=5)

            if codigo == "IDA":
                vistadome_ida_var = checkbox_var
            elif codigo == "RET":
                vistadome_retorno_var = checkbox_var
        
    elif tour == MachuPicchuByCar3D:
        opciones_tour = ["machu_picchu_code", "montaña"]

        tk.Label(ventana, text="Códigos Machupicchu:").pack(pady=5)
        machu_picchu_entry = tk.Entry(ventana)
        machu_picchu_entry.pack()

        tk.Label(ventana, text="Montaña:").pack(pady=5)
        montaña_var = tk.StringVar(value="0")

        ttk.Radiobutton(ventana, text="Wayna Picchu Mountain", variable=montaña_var, value="WAYNA PICCHU MOUNTAIN").pack()
        ttk.Radiobutton(ventana, text="Machu Picchu Mountain", variable=montaña_var, value="MACHU PICCHU MOUNTAIN").pack()
        
    elif tour == AmazonTour4D or tour == AmazonTour3D or tour == Choquequirao4Days or tour == Choquequirao3Days:
        pass

    elif tour == HumantayLakeFullDayTour or tour == RainbowMountainFullDayTour or tour == PalcoyoFullDayTour or tour == AusangateFullDayTour:
        opciones_tour = ["hotel"]
        
        tk.Label(ventana, text="Nombre del Hotel:").pack(pady=5)
        hotel_var = tk.StringVar()
        hotel_entry = tk.Entry(ventana, textvariable=hotel_var)
        hotel_entry.pack()

    elif tour == ValleSagradoFullDayTour or tour == MorayFullDayTour or tour == CuscoCityTour:
        opciones_tour = []
        tk.Label(ventana, text="No se requiere información del hotel para este tour.").pack(pady=10)
        
    tk.Label(ventana, text="Número de Teléfono (+código de país):").pack(pady=5)

    # Crear un Frame para alinear el cuadro de texto y el botón
    telefono_frame = tk.Frame(ventana)
    telefono_frame.pack(pady=5)

    telefono_entry = tk.Entry(telefono_frame, width=25)  # Ajustamos el ancho para que el botón encaje mejor
    telefono_entry.pack(side=tk.LEFT, padx=5)

    # Agregar el botón de formatear al lado del cuadro de texto
    formatear_btn = tk.Button(telefono_frame, text="F", command=lambda: formatear_numero(telefono_entry), width=3)
    formatear_btn.pack(side=tk.LEFT, padx=5)
    
    frame_botones = tk.Frame(ventana)
    frame_botones.pack(pady=10)
    tk.Button(frame_botones, text="Volver", command=menu_principal, bg="#ff8e8e").pack(side=tk.LEFT, padx=10)
    tk.Button(frame_botones, text="Enviar", command=enviar_datos , bg="#c1ff8e").pack(side=tk.LEFT, padx=10)
    
def fecha_nombre(dia_inicial, mes, año, dias_a_sumar=0):
    fecha_base = datetime(año, mes, dia_inicial)
    
    nueva_fecha = fecha_base + timedelta(days=dias_a_sumar)
    
    nombre_dias = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    nombre_dia = nombre_dias[nueva_fecha.weekday()]
    
    nombre_meses = ["January", "February", "March", "April", "May", 
                    "June", "July", "August", "September", "October", 
                    "November", "December"]
    
    dia = nueva_fecha.day
    if 11 <= dia <= 13:
        sufijo = "th"
    else:
        sufijos = {1: "st", 2: "nd", 3: "rd"}
        sufijo = sufijos.get(dia % 10, "th")
    
    fecha_texto = f"{nombre_dia}, {dia}{sufijo} {nombre_meses[nueva_fecha.month - 1]} {nueva_fecha.year}"
    return fecha_texto

def fecha_nombre_es(dia_inicial, mes, año, dias_a_sumar=0):
    fecha_base = datetime(año, mes, dia_inicial)
    
    nueva_fecha = fecha_base + timedelta(days=dias_a_sumar)
    
    nombre_dias_es = ["lunes", "martes", "miércoles", "jueves", "viernes", "sábado", "domingo"]
    nombre_dia_es = nombre_dias_es[nueva_fecha.weekday()]
    
    nombre_meses_es = ["enero", "febrero", "marzo", "abril", "mayo", 
                       "junio", "julio", "agosto", "septiembre", "octubre", 
                       "noviembre", "diciembre"]
    
    dia = nueva_fecha.day
    sufijo = "º"
    
    fecha_texto_es = f"{nombre_dia_es.capitalize()}, {dia}{sufijo} de {nombre_meses_es[nueva_fecha.month - 1]} de {nueva_fecha.year}"
    return fecha_texto_es

def ejecutar_en_consola_con_datos(tour, datos):
    print("DATOS:", datos)
    
    confirmacion = tour(datos)
    
    confirmacion.generar_confirmacion()
    
    limpiar_ventana(ventana)
    menu_principal()

def limpiar_ventana(ventana):
    """Limpia todos los widgets de una ventana"""
    for widget in ventana.winfo_children():
        widget.destroy()

def enviar_mensajes_whatsapp():
    for phone_number, message in mensajes_whatsapp:
        try:
            message_encoded = urllib.parse.quote(message)
            url = f"https://web.whatsapp.com/send?phone={phone_number}&text={message_encoded}"
            
        except Exception as e:
            print(f"Error al enviar mensaje a {phone_number}: {e}")

    # Vaciar la lista de mensajes después de enviar
    mensajes_whatsapp.clear()

def salir():
    global ventana, mensajes_whatsapp, stored_messages

    # Verificar si hay mensajes almacenados de recordatorio
    if stored_messages:  # Si hay mensajes de recordatorio almacenados
        respuesta_stored = tk.messagebox.askyesno(
            "Mensajes almacenados",
            "Hay mensajes almacenados de recordatorios. ¿Desea enviarlos ahora?"
        )
        if respuesta_stored:
            # Enviar los mensajes almacenados
            chrome_path = r"C:\Program Files\Google\Chrome\Application\chrome.exe %s"
            webbrowser.get(f'"{chrome_path}"').open_new_tab("https://web.whatsapp.com")

            for phone_number, message in stored_messages:
                try:
                    kit.sendwhatmsg_instantly(phone_number, message, tab_close=True, close_time=5)
                except Exception as e:
                    print(f"Error al enviar mensaje a {phone_number}: {e}")
            
            # Limpiar los mensajes después de enviarlos
            stored_messages.clear()
            print("Mensajes de recordatorio enviados con éxito.")
        else:
            print("El usuario decidió no enviar los mensajes almacenados de recordatorio.")

    # Verificar si hay mensajes de WhatsApp pendientes de enviar
    if mensajes_whatsapp:  # Si hay mensajes pendientes de enviar
        respuesta = tk.messagebox.askokcancel(
            "Envío de WhatsApp",
            "Se enviarán todos los mensajes de WhatsApp acumulados. ES NECESARIO QUE LA VENTANA DE WEB WHATSAPP ESTE AL FONDO!!!. La ventana se cerrará automáticamente cuando se complete. ¿Desea continuar?"
        )

        if respuesta:
            # Abrir WhatsApp Web
            chrome_path = r"C:\Program Files\Google\Chrome\Application\chrome.exe %s"
            webbrowser.get(f'"{chrome_path}"').open_new_tab("https://web.whatsapp.com")

            for phone_number, message in mensajes_whatsapp:
                try:
                    kit.sendwhatmsg_instantly(phone_number, message, tab_close=True, close_time=5)
                except Exception as e:
                    print(f"Error al enviar mensaje a {phone_number}: {e}")

            # Limpiar mensajes después de enviarlos
            mensajes_whatsapp.clear()

            if ventana is not None:
                ventana.quit()
                ventana.destroy()
                ventana = None
                print("Saliendo después de enviar mensajes.")
        else:
            print("El usuario canceló el envío de mensajes.")
    else:
        print("No hay mensajes pendientes.")
    
    # Finalizar el programa si no hay ventanas abiertas
    if ventana is not None:
        ventana.quit()
        ventana.destroy()
        ventana = None
        print("Saliendo del programa.")

def pre_menu():
    version = "V5.1.0 TEMPORADA 2025"

    global ventana, fondo_imagen
    if ventana is None or not ventana.winfo_exists():
        ajustar_dpi()
        ventana = tk.Tk()
    else:
        limpiar_ventana(ventana)

    ventana.title("MPR - Selección")
    ventana.geometry("250x300")
    ventana.iconbitmap(resource_path("logo_nuevo.ico"))
    ventana.resizable(False, False)
    ventana.attributes('-topmost', False)

    fondo = Image.open(resource_path("fondo3.jpg"))
    fondo = fondo.resize((250, 300), Image.Resampling.LANCZOS)
    fondo_imagen = ImageTk.PhotoImage(fondo)

    # Using Canvas in pre_menu
    canvas = tk.Canvas(ventana, width=250, height=300)
    canvas.pack(fill="both", expand=True)
    canvas.create_image(0, 0, image=fondo_imagen, anchor="nw")

    # Title
    canvas.create_text(125, 40, text="SELECCIONE\nUNA OPCIÓN", font=("Verdana", 12, "bold"), fill="Purple")

    # Buttons with even spacing
    canvas.create_window(125, 80, window=tk.Button(ventana, text="COMPACTO", command=menu_compacto, width=18, bg="#fff58e", font=("Verdana", 10)))
    canvas.create_window(125, 115, window=tk.Button(ventana, text="EXTENSO", command=menu_principal, width=18, bg="#fff58e", font=("Verdana", 10)))
    canvas.create_window(125, 150, window=tk.Button(ventana, text="RECORDATORIOS", command=recordatorio, width=18, bg="#8ebbff", font=("Verdana", 10)))
    canvas.create_window(125, 185, window=tk.Button(ventana, text="GAMES", command=games_menu, width=18, bg="#d3d3d3", font=("Verdana", 10)))  # Same style, different color
    canvas.create_window(125, 220, window=tk.Button(ventana, text="SALIR", command=salir, width=18, bg="#ff8e8e", font=("Verdana", 10)))

    # Version text
    canvas.create_text(245, 295, text=version, font=("Arial", 7), fill="Red", anchor="se")

    ventana.mainloop()

# Función para obtener la ruta de un recurso (funciona con PyInstaller)
def resource_path(relative_path):
    """Obtiene la ruta absoluta del recurso, funciona tanto en desarrollo como en PyInstaller."""
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath(os.path.dirname(__file__)), relative_path)

# Configuración de Google Sheets
SCOPE = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
CREDENTIALS_FILE = resource_path("credentials.json")
SHEET_ID = "1DvVOBoIL2FkrZWfrRX4WM2mFe7x577hadQC-5wp7se0"
SHEET_NAME = "Sheet1"

def get_google_sheet():
    try:
        creds = ServiceAccountCredentials.from_json_keyfile_name(CREDENTIALS_FILE, SCOPE)
        client = gspread.authorize(creds)
        sheet = client.open_by_key(SHEET_ID).worksheet(SHEET_NAME)
        return sheet
    except Exception as e:
        messagebox.showerror("Error de Autenticación", f"No se pudo conectar a Google Sheets: {str(e)}\nAsegúrate de que la hoja esté compartida con confirmaciones@stately-command-430404-c1.iam.gserviceaccount.com y que las APIs estén habilitadas.")
        raise

# Inicializar la hoja si está vacía
def initialize_sheet():
    try:
        sheet = get_google_sheet()
        # Obtener la primera fila (encabezados)
        current_headers = sheet.row_values(1)
        
        # Definir los encabezados esperados
        expected_headers = ["USUARIO", "CONTRASEÑA", "SCORE G1", "SCORE G2", "SCORE G3"]
        
        # Si la primera fila está vacía o no coincide con los encabezados esperados, inicializarla
        if not current_headers or current_headers != expected_headers:
            # Limpiar la primera fila si existe
            if current_headers:
                sheet.delete_rows(1)
            # Agregar los encabezados esperados
            sheet.append_row(expected_headers)
    except Exception as e:
        messagebox.showerror("Error", f"No se pudo inicializar la hoja: {str(e)}")
        raise

# Validar credenciales
def check_credentials(username, password):
    global current_username, current_password
    username = username.lower()
    password = password.lower()

    try:
        sheet = get_google_sheet()
        initialize_sheet()
        
        # Obtener todas las filas (incluidos los encabezados)
        all_rows = sheet.get_all_values()
        if len(all_rows) <= 1:  # Solo hay encabezados, no hay usuarios
            messagebox.showerror("Error", "No hay usuarios registrados.")
            return

        # Convertir las filas en una lista de diccionarios manualmente
        headers = all_rows[0]  # Primera fila son los encabezados
        records = []
        for row in all_rows[1:]:  # Saltar la primera fila (encabezados)
            record = {}
            for i, header in enumerate(headers):
                record[header] = row[i] if i < len(row) else ""
            records.append(record)

        # Buscar el usuario
        for record in records:
            if record["USUARIO"] == username and record["CONTRASEÑA"] == password:
                current_username = username
                current_password = password
                show_games()
                return
        messagebox.showerror("Error", "Usuario o contraseña incorrectos.")
    except Exception as e:
        print(f"Error al validar credenciales: {e}")
        messagebox.showerror("Error", f"No se pudo validar las credenciales: {str(e)}")

# Funciones para interactuar con Google Sheets
def get_high_score(username, game="SCORE G1"):
    try:
        sheet = get_google_sheet()
        initialize_sheet()
        records = sheet.get_all_records()
        for record in records:
            if record["USUARIO"] == username.lower():
                return record.get(game, 0)
        return 0
    except Exception as e:
        print(f"Error al obtener la puntuación: {e}")
        return 0

def save_score(username, password, score, game="SCORE G1"):
    try:
        sheet = get_google_sheet()
        initialize_sheet()
        records = sheet.get_all_records()
        user_exists = False
        for i, record in enumerate(records):
            if record["USUARIO"] == username.lower():
                user_exists = True
                if record["CONTRASEÑA"] == password.lower():
                    current_score = record.get(game, 0)
                    if score > current_score:
                        col_index = {"SCORE G1": 3, "SCORE G2": 4, "SCORE G3": 5}[game]
                        sheet.update_cell(i + 2, col_index, score)
                break
        if not user_exists:
            new_row = [username.lower(), password.lower(), 0, 0, 0]
            col_index = {"SCORE G1": 2, "SCORE G2": 3, "SCORE G3": 4}[game]
            new_row[col_index] = score
            sheet.append_row(new_row)
    except Exception as e:
        print(f"Error al guardar la puntuación: {e}")

def get_leaderboard(game="SCORE G1"):
    try:
        sheet = get_google_sheet()
        initialize_sheet()
        records = sheet.get_all_records()
        leaderboard = [(record["USUARIO"], record.get(game, 0)) for record in records]
        leaderboard.sort(key=lambda x: x[1], reverse=True)
        return leaderboard
    except Exception as e:
        print(f"Error al obtener el leaderboard: {e}")
        return []

# Validar y crear un nuevo usuario
def create_user(username, password):
    username = username.lower()
    password = password.lower()

    if not re.match("^[a-z0-9]+$", username):
        messagebox.showerror("Error", "El nombre de usuario debe contener solo letras y números.")
        return False

    if not any(c.isalpha() for c in password):
        messagebox.showerror("Error", "La contraseña debe contener al menos una letra.")
        return False

    try:
        sheet = get_google_sheet()
        initialize_sheet()
        records = sheet.get_all_records()
        for record in records:
            if record["USUARIO"] == username:
                messagebox.showerror("Error", "El usuario ya existe.")
                return False

        sheet.append_row([username, password, 0, 0, 0])
        messagebox.showinfo("Éxito", "Usuario creado exitosamente.")
        return True
    except Exception as e:
        print(f"Error al crear usuario: {e}")
        messagebox.showerror("Error", f"No se pudo crear el usuario: {str(e)}")
        return False
        
# Menú de inicio de sesión
def games_menu():
    global ventana
    limpiar_ventana(ventana)

    ventana.title("Iniciar Sesión")
    ventana.geometry("250x300")
    ventana.configure(bg="#f0f0f0")

    tk.Label(ventana, text="INGRESE CREDENCIALES", font=("Verdana", 12, "bold"), fg="Purple", bg="#f0f0f0").pack(pady=10)

    tk.Label(ventana, text="Usuario:", font=("Arial", 10), bg="#f0f0f0").pack()
    username_entry = tk.Entry(ventana)
    username_entry.pack(pady=5)

    tk.Label(ventana, text="Contraseña:", font=("Arial", 10), bg="#f0f0f0").pack()
    password_entry = tk.Entry(ventana, show="*")
    password_entry.pack(pady=5)

    tk.Button(ventana, text="Iniciar Sesión", command=lambda: check_credentials(username_entry.get(), password_entry.get()), bg="#8ebbff").pack(pady=10)
    tk.Button(ventana, text="Crear Usuario", command=lambda: create_user(username_entry.get(), password_entry.get()), bg="#90ee90").pack(pady=5)
    tk.Button(ventana, text="Volver", command=pre_menu, bg="#ff8e8e").pack(pady=5)

# Menú de juegos
def show_games():
    global ventana
    limpiar_ventana(ventana)

    ventana.title("Juegos")
    ventana.geometry("250x300")
    ventana.configure(bg="#f0f0f0")

    tk.Label(ventana, text="JUEGOS", font=("Verdana", 12, "bold"), fg="Purple", bg="#f0f0f0").pack(pady=10)
    tk.Button(ventana, text="Snake", command=lambda: start_game("snake"), width=18, bg="#fff58e").pack(pady=5)
    tk.Button(ventana, text="Juego 2", command=lambda: start_game("game2"), width=18, bg="#fff58e").pack(pady=5)
    tk.Button(ventana, text="Juego 3", command=lambda: start_game("game3"), width=18, bg="#fff58e").pack(pady=5)
    tk.Button(ventana, text="Volver", command=pre_menu, width=18, bg="#ff8e8e").pack(pady=10)

def start_game(game_name):
    ventana.withdraw()

    if game_name == "snake":
        run_snake_game()
    else:
        pygame.init()
        screen = pygame.display.set_mode((400, 300))
        pygame.display.set_caption(f"Jugando {game_name}")
        clock = pygame.time.Clock()

        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            screen.fill((0, 0, 0))
            font = pygame.font.Font(None, 36)
            text = font.render(f"{game_name} en progreso", True, (255, 255, 255))
            screen.blit(text, (100, 130))
            pygame.display.flip()
            clock.tick(60)

        pygame.quit()

    ventana.deiconify()
    show_games()

def run_snake_game():
    pygame.init()
    screen_width, screen_height = 600, 400
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("Snake Game")
    clock = pygame.time.Clock()

    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    RED = (255, 0, 0)
    GREEN = (0, 255, 0)

    def snake_pre_menu():
        high_score = get_high_score(current_username, "SCORE G1")
        font = pygame.font.Font(None, 36)
        small_font = pygame.font.Font(None, 24)

        button_width, button_height = 200, 50
        start_button = pygame.Rect(screen_width//2 - button_width//2, 150, button_width, button_height)
        leaderboard_button = pygame.Rect(screen_width//2 - button_width//2, 210, button_width, button_height)
        exit_button = pygame.Rect(screen_width//2 - button_width//2, 270, button_width, button_height)

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return "exit"
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = event.pos
                    if start_button.collidepoint(mouse_pos):
                        return "start"
                    elif leaderboard_button.collidepoint(mouse_pos):
                        return "leaderboard"
                    elif exit_button.collidepoint(mouse_pos):
                        return "exit"

            screen.fill(BLACK)
            welcome_text = font.render(f"Bienvenido {current_username}", True, WHITE)
            score_text = small_font.render(f"Tu mayor puntuación: {high_score}", True, WHITE)
            screen.blit(welcome_text, (screen_width//2 - welcome_text.get_width()//2, 50))
            screen.blit(score_text, (screen_width//2 - score_text.get_width()//2, 100))

            pygame.draw.rect(screen, GREEN, start_button)
            pygame.draw.rect(screen, WHITE, leaderboard_button)
            pygame.draw.rect(screen, RED, exit_button)

            start_text = small_font.render("Iniciar Juego", True, BLACK)
            leaderboard_text = small_font.render("Ver Clasificaciones", True, BLACK)
            exit_text = small_font.render("Salir", True, BLACK)

            screen.blit(start_text, (start_button.x + (button_width - start_text.get_width())//2, start_button.y + (button_height - start_text.get_height())//2))
            screen.blit(leaderboard_text, (leaderboard_button.x + (button_width - leaderboard_text.get_width())//2, leaderboard_button.y + (button_height - leaderboard_text.get_height())//2))
            screen.blit(exit_text, (exit_button.x + (button_width - exit_text.get_width())//2, exit_button.y + (button_height - exit_text.get_height())//2))

            pygame.display.flip()
            clock.tick(60)

    def show_leaderboard():
        leaderboard = get_leaderboard("SCORE G1")
        font = pygame.font.Font(None, 36)
        small_font = pygame.font.Font(None, 24)

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return "exit"
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        return "back"

            screen.fill(BLACK)
            title_text = font.render("Clasificaciones", True, WHITE)
            screen.blit(title_text, (screen_width//2 - title_text.get_width()//2, 50))

            for i, (player, score) in enumerate(leaderboard[:5]):
                entry_text = small_font.render(f"{i+1}. {player}: {score}", True, WHITE)
                screen.blit(entry_text, (screen_width//2 - entry_text.get_width()//2, 100 + i*40))

            back_text = small_font.render("Presiona ESC para volver", True, WHITE)
            screen.blit(back_text, (screen_width//2 - back_text.get_width()//2, screen_height - 50))

            pygame.display.flip()
            clock.tick(60)

    def snake_game():
        snake_block = 20
        snake_speed = 15
        snake_list = []
        length_of_snake = 1
        x1, y1 = screen_width // 2, screen_height // 2
        dx, dy = snake_block, 0
        snake_head = [x1, y1]

        apple_x = round(random.randrange(0, screen_width - snake_block) / snake_block) * snake_block
        apple_y = round(random.randrange(0, screen_height - snake_block) / snake_block) * snake_block

        score = 0
        font = pygame.font.Font(None, 36)

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return score
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT and dx != snake_block:
                        dx, dy = -snake_block, 0
                    elif event.key == pygame.K_RIGHT and dx != -snake_block:
                        dx, dy = snake_block, 0
                    elif event.key == pygame.K_UP and dy != snake_block:
                        dx, dy = 0, -snake_block
                    elif event.key == pygame.K_DOWN and dy != -snake_block:
                        dx, dy = 0, snake_block

            x1 += dx
            y1 += dy

            if x1 >= screen_width:
                x1 = 0
            elif x1 < 0:
                x1 = screen_width - snake_block
            if y1 >= screen_height:
                y1 = 0
            elif y1 < 0:
                y1 = screen_height - snake_block

            snake_head = [x1, y1]
            snake_list.append(snake_head)

            if len(snake_list) > length_of_snake:
                del snake_list[0]

            for segment in snake_list[:-1]:
                if segment == snake_head:
                    return score

            if x1 == apple_x and y1 == apple_y:
                apple_x = round(random.randrange(0, screen_width - snake_block) / snake_block) * snake_block
                apple_y = round(random.randrange(0, screen_height - snake_block) / snake_block) * snake_block
                length_of_snake += 1
                score += 1
                snake_speed += 1

            screen.fill(BLACK)
            pygame.draw.rect(screen, RED, [apple_x, apple_y, snake_block, snake_block])
            for segment in snake_list:
                pygame.draw.rect(screen, GREEN, [segment[0], segment[1], snake_block, snake_block])

            score_text = font.render(f"Score: {score}", True, WHITE)
            screen.blit(score_text, (10, 10))

            pygame.display.flip()
            clock.tick(snake_speed)

    while True:
        action = snake_pre_menu()
        if action == "start":
            score = snake_game()
            save_score(current_username, current_password, score, "SCORE G1")
        elif action == "leaderboard":
            result = show_leaderboard()
            if result == "exit":
                break
        elif action == "exit":
            break

    pygame.quit()
    
# Definición vacía de menu_compacto para que trabajes en ella
def menu_compacto():
    global ventana

    if ventana is None or not ventana.winfo_exists():
        ajustar_dpi()
        ventana = tk.Tk()
        ventana.title("MPR - Compacto")
        ventana.geometry("250x350")
        ventana.iconbitmap(resource_path("logo_nuevo.ico"))
        ventana.resizable(False, False)
        ventana.attributes('-topmost', True)
    else:
        limpiar_ventana(ventana)
        ventana.title("MPR - Compacto")
        ventana.geometry("250x350")
        ventana.iconbitmap(resource_path("logo_nuevo.ico"))
        ventana.resizable(False, False)
        ventana.attributes('-topmost', True)

    tours = [
        "Salkantay5D", "Salkantay4D", "Salkantay3D", "Salkantay2D", "Llactapata3D",
        "IncaTrail4D", "IncaTrail2D", "IncaTrail1D", "IncaJungle4D", "IncaJungle3D",
        "MachuPicchuFullDay", "MachuPicchu2DTrain", "SacredValleyMachuPicchu2D",
        "MachuPicchuByCar2D", "MachuPicchuByCarTrain2D", "MachuPicchuByCar3D",
        "AmazonTour4D", "AmazonTour3D", "Choquequirao4Days", "Choquequirao3Days",
        "HumantayLakeFullDayTour", "RainbowMountainFullDayTour", "PalcoyoFullDayTour",
        "ValleSagradoFullDayTour", "MorayFullDayTour", "CuscoCityTour", "AusangateFullDayTour"
    ]
    nombres_tours_compacto = {
        "Salkantay5D": "Salkantay 5D", "Salkantay4D": "Salkantay 4D",
        "Salkantay3D": "Salkantay 3D", "Salkantay2D": "Salkantay 2D",
        "Llactapata3D": "Llactapata 3D", "IncaTrail4D": "Inca Trail 4D",
        "IncaTrail2D": "Inca Trail 2D", "IncaTrail1D": "Inca Trail 1D",
        "IncaJungle4D": "Inca Jungle 4D", "IncaJungle3D": "Inca Jungle 3D",
        "MachuPicchuFullDay": "Machu Picchu Full Day", "MachuPicchu2DTrain": "Machu Picchu 2D by train",
        "SacredValleyMachuPicchu2D": "Sacred Valley + Machu Picchu",
        "MachuPicchuByCar2D": "Machu Picchu 2D by car", "MachuPicchuByCarTrain2D": "Machu Picchu 2D by car by train",
        "MachuPicchuByCar3D": "Machu Picchu 3D by car", "AmazonTour4D": "Amazon Manu 4D",
        "AmazonTour3D": "Amazon Manu 3D", "Choquequirao4Days": "Choquequirao 4D",
        "Choquequirao3Days": "Choquequirao 3D", "HumantayLakeFullDayTour": "Humantay Lake",
        "RainbowMountainFullDayTour": "Rainbow Mountain", "PalcoyoFullDayTour": "Palcoyo",
        "ValleSagradoFullDayTour": "Valle Sagrado", "MorayFullDayTour": "Moray",
        "CuscoCityTour": "Cusco City", "AusangateFullDayTour": "Ausangate 7 Lakes"
    }

    no_machu_picchu_no_balance_tours = [
        "HumantayLakeFullDayTour", "RainbowMountainFullDayTour", "PalcoyoFullDayTour",
        "ValleSagradoFullDayTour", "MorayFullDayTour", "CuscoCityTour", "AusangateFullDayTour"
    ]

    def refrescar_ventana(selected_tour_name):
        for widget in ventana.winfo_children():
            if widget != titulo_label and widget != tour_menu:
                widget.destroy()

        def validar_fecha(event):
            texto = fecha_entry.get()
            #permitido = "0123456789/"
            #if event.char and event.char not in permitido:
                #return "break"

        def validar_nombres(event):
            texto = nombres_entry.get()
            #permitido = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ, "
            #if event.char and event.char not in permitido:
                #return "break"

        def validar_balance(event):
            texto = balance_entry.get()
            #permitido = "0123456789"
            #if event.char and event.char not in permitido:
                #return "break"

        tk.Label(ventana, text="Fecha (d/m/a):", font=("Verdana", 7)).pack(pady=2)
        fecha_entry = tk.Entry(ventana, width=15, font=("Verdana", 7))
        fecha_entry.pack(pady=2)
        fecha_entry.bind("<KeyPress>", validar_fecha)

        tk.Label(ventana, text="Nombres:", font=("Verdana", 7)).pack(pady=2)
        nombres_entry = tk.Entry(ventana, width=25, font=("Verdana", 7))
        nombres_entry.pack(pady=2)
        nombres_entry.bind("<KeyPress>", validar_nombres)

        selected_tour = next(tour for tour in tours if nombres_tours_compacto[tour] == selected_tour_name)
        if selected_tour not in no_machu_picchu_no_balance_tours:
            tk.Label(ventana, text="Código M. Picchu:", font=("Verdana", 7)).pack(pady=2)
            machu_picchu_entry = tk.Entry(ventana, width=25, font=("Verdana", 7))
            machu_picchu_entry.pack(pady=2)
            tk.Label(ventana, text="Balance ($):", font=("Verdana", 7)).pack(pady=2)
            balance_entry = tk.Entry(ventana, width=15, font=("Verdana", 7))
            balance_entry.pack(pady=2)
            balance_entry.bind("<KeyPress>", validar_balance)
        else:
            machu_picchu_entry = None
            balance_entry = None

        def enviar_datos_compacto():
            try:
                if not nombres_entry.get().strip():
                    tk.messagebox.showwarning("Error", "Por favor, ingrese al menos un nombre.")
                    return
                if not fecha_entry.get().strip():
                    tk.messagebox.showwarning("Error", "Por favor, ingrese una fecha.")
                    return

                nombres = [nombre.strip().upper() for nombre in nombres_entry.get().split(',') if nombre.strip()]
                for nombre in nombres:
                    if any(char.isdigit() or char in "!@#$%^&*()_+-=[]{}|;:.<>?" for char in nombre):
                        tk.messagebox.showwarning("Error", f"El nombre '{nombre}' solo puede contener letras.")
                        return

                try:
                    fecha = tuple(map(int, fecha_entry.get().split('/')))
                    if len(fecha) != 3 or not (1 <= fecha[0] <= 31) or not (1 <= fecha[1] <= 12):
                        raise ValueError
                except ValueError:
                    tk.messagebox.showwarning("Error", "Fecha no válida. Use formato día/mes/año.")
                    return

                balance = 0
                if selected_tour not in no_machu_picchu_no_balance_tours:
                    try:
                        balance_input = balance_entry.get().strip()
                        balance = int(balance_input) if balance_input else 0
                        if balance < 0:
                            raise ValueError
                    except ValueError:
                        tk.messagebox.showwarning("Error", "El balance debe ser un número entero positivo.")
                        return

                fecha_inicial = datetime(fecha[2], fecha[1], fecha[0]).date()
                fecha_actual = datetime.now().date()

                tour_dias = {
                    "Salkantay5D": 4, "Salkantay4D": 3, "Salkantay3D": 2, "Salkantay2D": 1,
                    "Llactapata3D": 2, "IncaTrail4D": 3, "IncaTrail2D": 1, "IncaTrail1D": 0,
                    "IncaJungle4D": 3, "IncaJungle3D": 2, "MachuPicchuFullDay": 0,
                    "MachuPicchu2DTrain": 1, "SacredValleyMachuPicchu2D": 1, "MachuPicchuByCar2D": 1,
                    "MachuPicchuByCarTrain2D": 1, "MachuPicchuByCar3D": 2, "AmazonTour4D": 3,
                    "AmazonTour3D": 2, "Choquequirao4Days": 3, "Choquequirao3Days": 2,
                    "HumantayLakeFullDayTour": 0, "RainbowMountainFullDayTour": 0,
                    "PalcoyoFullDayTour": 0, "ValleSagradoFullDayTour": 0, "MorayFullDayTour": 0,
                    "CuscoCityTour": 0, "AusangateFullDayTour": 0
                }
                dias_tour = tour_dias.get(selected_tour, 1)

                if fecha_inicial < fecha_actual:
                    tk.messagebox.showwarning("Error", "No se pueden confirmar fechas pasadas.")
                    return
                elif fecha_inicial == fecha_actual and dias_tour > 0:
                    tk.messagebox.showwarning("Error", "Tour no Full Day debe ser mínimo para mañana.")
                    return

                machu_picchu_code = "0"
                if selected_tour not in no_machu_picchu_no_balance_tours:
                    machu_picchu_code = machu_picchu_entry.get().strip() or "0"
                    if selected_tour in ["IncaTrail4D", "IncaTrail2D", "IncaTrail1D"] and machu_picchu_code == "0":
                        tk.messagebox.showwarning("Error", "Los tours Camino Inca requieren al menos un código válido.")
                        return
                    if machu_picchu_code != "0":
                        if len(machu_picchu_code) >= 6:
                            codigo_fecha = machu_picchu_code[:6]
                            codigo_dia, codigo_mes, codigo_ano = int(codigo_fecha[:2]), int(codigo_fecha[2:4]), int(codigo_fecha[4:6])
                            fecha_codigo = datetime(2000 + codigo_ano, codigo_mes, codigo_dia).date()
                        else:
                            tk.messagebox.showwarning("Error", "Formato de código Machu Picchu incorrecto.")
                            return

                        if selected_tour == "MachuPicchuByCar3D":
                            fecha_ingreso_machu_picchu = fecha_inicial + timedelta(days=1)
                        else:
                            fecha_ingreso_machu_picchu = fecha_inicial + timedelta(days=dias_tour)

                        if selected_tour in ["IncaTrail4D", "IncaTrail2D", "IncaTrail1D"]:
                            if fecha_codigo != fecha_inicial:
                                tk.messagebox.showwarning("Error", "El código debe coincidir con la fecha de inicio.")
                                return
                        elif fecha_codigo != fecha_ingreso_machu_picchu:
                            tk.messagebox.showwarning("Error", "El código no coincide con la fecha de ingreso a Machu Picchu.")
                            return

                datos = {
                    "nombres": nombres,
                    "fecha": fecha,
                    "machu_picchu_code": machu_picchu_code,
                    "tour": selected_tour,
                    "balance": balance
                }
                generar_confirmacion_tour_compacto(selected_tour, datos)
                fecha_entry.delete(0, tk.END)
                nombres_entry.delete(0, tk.END)
                if machu_picchu_entry:
                    machu_picchu_entry.delete(0, tk.END)
                if balance_entry:
                    balance_entry.delete(0, tk.END)

            except Exception as e:
                tk.messagebox.showwarning("Error", f"Ocurrió un error: {str(e)}")

        btn_frame = tk.Frame(ventana)
        btn_frame.pack(pady=5)
        tk.Button(btn_frame, text="Volver", command=pre_menu, width=8, bg="#ff8e8e").pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="Enviar", command=enviar_datos_compacto, width=8, bg="#c1ff8e").pack(side=tk.LEFT, padx=5)

        tk.Button(ventana, text="Ver Confi", command=ver_confirmacion, width=15, bg="#c1ff8e").pack(pady=5)

    titulo_label = tk.Label(ventana, text="CONFIRMACION COMPACTA", font=("Verdana", 9, "bold"), fg="purple")
    titulo_label.pack(pady=2)

    tour_var = tk.StringVar(ventana)
    tour_var.set(nombres_tours_compacto[tours[0]])
    tour_menu = tk.OptionMenu(ventana, tour_var, *[nombres_tours_compacto[tour] for tour in tours])
    tour_menu.config(font=("Verdana", 7), width=25)
    tour_menu.pack(pady=2)

    refrescar_ventana(tour_var.get())
    tour_var.trace("w", lambda *args: refrescar_ventana(tour_var.get()))

    ventana.mainloop()

def generar_confirmacion_tour_compacto(tour, datos):
    nombres_tours_completos = {
        "Salkantay5D": "Salkantay Trek to Machu Picchu 5D-4N",
        "Salkantay4D": "Salkantay Trek to Machu Picchu 4D-3N",
        "Salkantay3D": "Salkantay Trek to Machu Picchu 3D-2N",
        "Salkantay2D": "Salkantay Trek 2D-1N",
        "Llactapata3D": "Llactapata Trek to Machu Picchu 3D-2N",
        "IncaTrail4D": "Inca Trail to Machu Picchu 4D-3N",
        "IncaTrail2D": "Inca Trail to Machu Picchu 2D-1N",
        "IncaTrail1D": "Inca Trail to Machu Picchu 1D",
        "IncaJungle4D": "Inca Jungle to Machu Picchu 4D-3N",
        "IncaJungle3D": "Inca Jungle to Machu Picchu 3D-2N",
        "MachuPicchuFullDay": "Machu Picchu Full Day",
        "MachuPicchu2DTrain": "Machu Picchu by Train 2D-1N",
        "SacredValleyMachuPicchu2D": "Sacred Valley + Machu Picchu 2D-1N",
        "MachuPicchuByCar2D": "Machu Picchu by Car 2D-1N",
        "MachuPicchuByCarTrain2D": "Machu Picchu by Car and Train 2D-1N",
        "MachuPicchuByCar3D": "Machu Picchu by Car 3D-2N",
        "AmazonTour4D": "Amazon Manu 4D-3N",
        "AmazonTour3D": "Amazon Manu 3D-2N",
        "Choquequirao4Days": "Choquequirao Trek 4D-3N",
        "Choquequirao3Days": "Choquequirao Trek 3D-2N",
        "HumantayLakeFullDayTour": "Humantay Lake Full Day",
        "RainbowMountainFullDayTour": "Rainbow Mountain Full Day",
        "PalcoyoFullDayTour": "Palcoyo Full Day",
        "ValleSagradoFullDayTour": "Valle Sagrado Full Day",
        "MorayFullDayTour": "Moray Full Day",
        "CuscoCityTour": "Cusco City Tour",
        "AusangateFullDayTour": "Ausangate 7 Lakes Full Day"
    }

    tour_dias = {
        "Salkantay5D": 4, "Salkantay4D": 3, "Salkantay3D": 2, "Salkantay2D": 1,
        "Llactapata3D": 2, "IncaTrail4D": 3, "IncaTrail2D": 1, "IncaTrail1D": 0,
        "IncaJungle4D": 3, "IncaJungle3D": 2, "MachuPicchuFullDay": 0,
        "MachuPicchu2DTrain": 1, "SacredValleyMachuPicchu2D": 1, "MachuPicchuByCar2D": 1,
        "MachuPicchuByCarTrain2D": 1, "MachuPicchuByCar3D": 2, "AmazonTour4D": 3,
        "AmazonTour3D": 2, "Choquequirao4Days": 3, "Choquequirao3Days": 2,
        "HumantayLakeFullDayTour": 0, "RainbowMountainFullDayTour": 0,
        "PalcoyoFullDayTour": 0, "ValleSagradoFullDayTour": 0, "MorayFullDayTour": 0,
        "CuscoCityTour": 0, "AusangateFullDayTour": 0
    }

    no_machu_picchu_tours = [
        "Salkantay2D", "Choquequirao4Days", "Choquequirao3Days", "AmazonTour4D", "AmazonTour3D",
        "HumantayLakeFullDayTour", "RainbowMountainFullDayTour", "PalcoyoFullDayTour",
        "ValleSagradoFullDayTour", "MorayFullDayTour", "CuscoCityTour", "AusangateFullDayTour"
    ]

    color_tour = "#FF4500"
    color_fechas = "#00B7EB"
    color_briefing = "#32CD32"
    color_texto = "#333333"
    color_saldo = "#FF6347"

    primer_nombre = datos['nombres'][0].split()[0].capitalize()
    nombre_tour = nombres_tours_completos.get(tour, tour)
    dias = tour_dias.get(tour, 1)
    fecha_inicio = datetime(datos['fecha'][2], datos['fecha'][1], datos['fecha'][0]).date()
    fecha_fin = fecha_inicio + timedelta(days=dias) if dias > 0 else fecha_inicio
    fecha_briefing = fecha_inicio - timedelta(days=1)

    def formato_fecha(fecha):
        return fecha.strftime("%d %B %Y")

    contenido = f"""
    <div style="max-width: 600px; margin: 0 auto; padding: 20px; border: 2px solid #00aaff; border-radius: 10px; box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1); background-color: #ffffff;">
        <h1 style="color: {color_tour}; text-align: center; font-size: 24px; margin-bottom: 20px;">Tour Confirmation</h1>
        <p style="color: {color_texto}; font-size: 16px; text-align: center;">Dear <strong>{primer_nombre}</strong>,</p>
        <p style="color: {color_texto}; font-size: 14px; text-align: center;">We are excited to confirm your adventure!</p>
        
        <div style="background-color: #f9f9f9; padding: 15px; border-radius: 8px; margin: 15px 0;">
            <p style="color: {color_tour}; font-size: 18px; font-weight: bold; text-align: center;">{nombre_tour}</p>
        </div>
    """

    if dias > 0:
        contenido += f"""
        <div style="border-left: 4px solid {color_fechas}; padding-left: 15px; margin: 15px 0;">
            <p style="color: {color_fechas}; font-size: 16px; font-weight: bold;">TRIP DATES</p>
            <p style="color: {color_texto}; margin: 5px 0;">Start: <strong>{formato_fecha(fecha_inicio)}</strong></p>
            <p style="color: {color_texto}; margin: 5px 0;">End: <strong>{formato_fecha(fecha_fin)}</strong></p>
        </div>
        """
    else:
        contenido += f"""
        <div style="border-left: 4px solid {color_fechas}; padding-left: 15px; margin: 15px 0;">
            <p style="color: {color_fechas}; font-size: 16px; font-weight: bold;">TRIP DATE</p>
            <p style="color: {color_texto}; margin: 5px 0;"><strong>{formato_fecha(fecha_inicio)}</strong></p>
        </div>
        """

    mensaje_base = "Our office in Cusco is open daily from 7:00 AM to 10:00 PM. Feel free to stop by upon arrival to receive more information"
    if tour in no_machu_picchu_tours and datos['machu_picchu_code'] == "0":
        mensaje_briefing = mensaje_base
    else:
        mensaje_briefing = f"{mensaje_base} AND PICK UP YOUR CORRESPONDING TICKETS"

    contenido += f"""
    <div style="border-left: 4px solid {color_briefing}; padding-left: 15px; margin: 15px 0;">
        <p style="color: {color_briefing}; font-size: 16px; font-weight: bold;">BRIEFING</p>
        <p style="color: {color_texto}; margin: 5px 0;">{mensaje_briefing}</p>
    </div>
    """

    contenido += f"""
    <div style="margin: 15px 0;">
        <p style="color: {color_texto}; font-size: 16px; font-weight: bold;">PARTICIPANTS ({len(datos['nombres']):02})</p>
        <ul style="margin-left: 20px; color: {color_texto}; font-size: 14px;">
            {''.join([f"<li>{i+1}. {nombre.strip().upper()}</li>" for i, nombre in enumerate(datos['nombres'])])}
        </ul>
    </div>
    """

    if datos['machu_picchu_code'] != "0":
        contenido += f"""
        <div style="border-left: 4px solid {color_tour}; padding-left: 15px; margin: 15px 0;">
            <p style="color: {color_tour}; font-size: 16px; font-weight: bold;">MACHU PICCHU ENTRY CODE</p>
            <p style="color: {color_texto}; margin: 5px 0;"><strong>{datos['machu_picchu_code']}</strong></p>
        </div>
        """
    else:
        contenido += f"""
        <div style="border-left: 4px solid {color_tour}; padding-left: 15px; margin: 15px 0;">
            <p style="color: {color_tour}; font-size: 16px; font-weight: bold;">MACHU PICCHU ENTRY</p>
            <p style="color: {color_texto}; margin: 5px 0;"><strong>DOES NOT INCLUDE MACHU PICCHU ENTRY</strong></p>
        </div>
        """

    if datos['saldo'] != "0":
        contenido += f"""
        <div style="border-left: 4px solid {color_saldo}; padding-left: 15px; margin: 15px 0;">
            <p style="color: {color_saldo}; font-size: 16px; font-weight: bold;">BALANCE PENDING</p>
            <p style="color: {color_texto}; margin: 5px 0;"><strong>${datos['saldo']}</strong></p>
        </div>
        """

    contenido += f"""
        <div style="text-align: center; margin-top: 20px; padding-top: 10px; border-top: 1px solid #ccc;">
            <p style="color: {color_texto}; font-size: 12px;">Machu Picchu Reservations | Contact us: <a href="https://wa.me/51908851429" style="color: {color_tour};">+51 908 851 429</a></p>
            <p style="color: {color_texto}; font-size: 12px;">Office location: Calle Plateros 316, Cusco, Peru</p>
        </div>
    </div>
    """

    nombre_archivo = "confirmacion.html"
    with open(nombre_archivo, "w", encoding="utf-8") as file:
        file.write(f"""
        <html>
        <head>
            <title>Confirmación de Reserva</title>
            <style>
                body {{ font-family: 'Verdana', sans-serif; background-color: #f0f0f0; margin: 20px; }}
                p {{ line-height: 1.6; }}
                ul {{ list-style-type: none; padding-left: 0; }}
                ul li::before {{ content: "✔"; color: {color_tour}; font-weight: bold; display: inline-block; width: 1em; margin-left: -1em; }}
            </style>
        </head>
        <body>
            {contenido}
        </body>
        </html>
        """)
    print(f"Confirmación guardada como {nombre_archivo}")

def generar_confirmacion_tour_compacto(tour, datos):
    nombres_tours_completos = {
        "Salkantay5D": "Salkantay Trek to Machu Picchu 5D-4N",
        "Salkantay4D": "Salkantay Trek to Machu Picchu 4D-3N",
        "Salkantay3D": "Salkantay Trek to Machu Picchu 3D-2N",
        "Salkantay2D": "Salkantay Trek 2D-1N",
        "Llactapata3D": "Llactapata Trek to Machu Picchu 3D-2N",
        "IncaTrail4D": "Inca Trail to Machu Picchu 4D-3N",
        "IncaTrail2D": "Inca Trail to Machu Picchu 2D-1N",
        "IncaTrail1D": "Inca Trail to Machu Picchu 1D",
        "IncaJungle4D": "Inca Jungle to Machu Picchu 4D-3N",
        "IncaJungle3D": "Inca Jungle to Machu Picchu 3D-2N",
        "MachuPicchuFullDay": "Machu Picchu Full Day",
        "MachuPicchu2DTrain": "Machu Picchu 2D-1N",
        "SacredValleyMachuPicchu2D": "Sacred Valley + Machu Picchu 2D-1N",
        "MachuPicchuByCar2D": "Machu Picchu by Car 2D-1N",
        "MachuPicchuByCarTrain2D": "Machu Picchu by Car and Train 2D-1N",
        "MachuPicchuByCar3D": "Machu Picchu by Car 3D-2N",
        "AmazonTour4D": "Amazon Manu 4D-3N",
        "AmazonTour3D": "Amazon Manu 3D-2N",
        "Choquequirao4Days": "Choquequirao Trek 4D-3N",
        "Choquequirao3Days": "Choquequirao Trek 3D-2N",
        "HumantayLakeFullDayTour": "Humantay Lake Full Day",
        "RainbowMountainFullDayTour": "Rainbow Mountain Full Day",
        "PalcoyoFullDayTour": "Palcoyo Full Day",
        "ValleSagradoFullDayTour": "Valle Sagrado Full Day",
        "MorayFullDayTour": "Moray Full Day",
        "CuscoCityTour": "Cusco City Tour",
        "AusangateFullDayTour": "Ausangate 7 Lakes Full Day"
    }

    tour_dias = {
        "Salkantay5D": 4, "Salkantay4D": 3, "Salkantay3D": 2, "Salkantay2D": 1,
        "Llactapata3D": 2, "IncaTrail4D": 3, "IncaTrail2D": 1, "IncaTrail1D": 0,
        "IncaJungle4D": 3, "IncaJungle3D": 2, "MachuPicchuFullDay": 0,
        "MachuPicchu2DTrain": 1, "SacredValleyMachuPicchu2D": 1, "MachuPicchuByCar2D": 1,
        "MachuPicchuByCarTrain2D": 1, "MachuPicchuByCar3D": 2, "AmazonTour4D": 3,
        "AmazonTour3D": 2, "Choquequirao4Days": 3, "Choquequirao3Days": 2,
        "HumantayLakeFullDayTour": 0, "RainbowMountainFullDayTour": 0,
        "PalcoyoFullDayTour": 0, "ValleSagradoFullDayTour": 0, "MorayFullDayTour": 0,
        "CuscoCityTour": 0, "AusangateFullDayTour": 0
    }

    no_machu_picchu_no_balance_tours = [
        "HumantayLakeFullDayTour", "RainbowMountainFullDayTour", "PalcoyoFullDayTour",
        "ValleSagradoFullDayTour", "MorayFullDayTour", "CuscoCityTour", "AusangateFullDayTour"
    ]

    color_tour = "#FF4500"
    color_fechas = "#00B7EB"
    color_briefing = "#32CD32"
    color_texto = "#333333"

    primer_nombre = datos['nombres'][0].split()[0].capitalize()
    nombre_tour = nombres_tours_completos.get(tour, tour)
    dias = tour_dias.get(tour, 1)
    fecha_inicio = datetime(datos['fecha'][2], datos['fecha'][1], datos['fecha'][0]).date()
    fecha_fin = fecha_inicio + timedelta(days=dias) if dias > 0 else fecha_inicio
    fecha_briefing = fecha_inicio - timedelta(days=1)
    balance = datos['balance']

    def formato_fecha(fecha):
        dias_semana = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
        dia_semana = dias_semana[fecha.weekday()]
        return f"{dia_semana} {fecha.day} {fecha.strftime('%B')} {fecha.year}"

    contenido = f"""
    <div style="max-width: 600px; margin: 0 auto; padding: 20px; border: 2px solid #00aaff; border-radius: 10px; box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1); background-color: #ffffff;">
        <h1 style="color: {color_tour}; text-align: center; font-size: 24px; margin-bottom: 20px;">Tour Confirmation</h1>
        <p style="color: {color_texto}; font-size: 16px; text-align: center;">Dear <strong>{primer_nombre}</strong>,</p>
        <p style="color: {color_texto}; font-size: 14px; text-align: center;">We are excited to confirm your adventure!</p>
        
        <div style="background-color: #f9f9f9; padding: 15px; border-radius: 8px; margin: 15px 0;">
            <p style="color: {color_tour}; font-size: 18px; font-weight: bold; text-align: center;">{nombre_tour}</p>
        </div>
    """

    if dias > 0:
        contenido += f"""
        <div style="border-left: 4px solid {color_fechas}; padding-left: 15px; margin: 15px 0;">
            <p style="color: {color_fechas}; font-size: 16px; font-weight: bold;">TRIP DATES</p>
            <p style="color: {color_texto}; margin: 5px 0;">Start: <strong>{formato_fecha(fecha_inicio)}</strong></p>
            <p style="color: {color_texto}; margin: 5px 0;">End: <strong>{formato_fecha(fecha_fin)}</strong></p>
        </div>
        """
    else:
        contenido += f"""
        <div style="border-left: 4px solid {color_fechas}; padding-left: 15px; margin: 15px 0;">
            <p style="color: {color_fechas}; font-size: 16px; font-weight: bold;">TRIP DATE</p>
            <p style="color: {color_texto}; margin: 5px 0;"><strong>{formato_fecha(fecha_inicio)}</strong></p>
        </div>
        """

    mensaje_base = "Our office in Cusco is open daily from 7:00 AM to 10:00 PM. Feel free to stop by upon arrival to receive more information"
    if tour in no_machu_picchu_no_balance_tours and datos['machu_picchu_code'] == "0":
        mensaje_briefing = mensaje_base
    else:
        mensaje_briefing = f"{mensaje_base} and pick up your corresponding tickets."

    contenido += f"""
    <div style="border-left: 4px solid {color_briefing}; padding-left: 15px; margin: 15px 0;">
        <p style="color: {color_briefing}; font-size: 16px; font-weight: bold;">BRIEFING</p>
        <p style="color: {color_texto}; margin: 5px 0;">{mensaje_briefing}</p>
    </div>
    """

    contenido += f"""
    <div style="margin: 15px 0;">
        <p style="color: {color_texto}; font-size: 16px; font-weight: bold;">PARTICIPANTS ({len(datos['nombres']):02})</p>
        <ul style="margin-left: 20px; color: {color_texto}; font-size: 14px;">
            {''.join([f"<li>{i+1}. {nombre.strip().upper()}</li>" for i, nombre in enumerate(datos['nombres'])])}
        </ul>
    </div>
    """

    if datos['machu_picchu_code'] != "0":
        contenido += f"""
        <div style="border-left: 4px solid {color_tour}; padding-left: 15px; margin: 15px 0;">
            <p style="color: {color_tour}; font-size: 16px; font-weight: bold;">MACHU PICCHU ENTRY CODE</p>
            <p style="color: {color_texto}; margin: 5px 0;"><strong>{datos['machu_picchu_code']}</strong></p>
        </div>
        """

    if balance > 0 and tour not in no_machu_picchu_no_balance_tours:
        contenido += f"""
        <div style="border-left: 4px solid {color_texto}; padding-left: 15px; margin: 15px 0;">
            <p style="color: {color_texto}; font-size: 16px; font-weight: bold;">BALANCE</p>
            <p style="color: {color_texto}; margin: 5px 0;"><strong>${balance}</strong></p>
            <p style="color: {color_texto}; font-size: 12px; margin: 5px 0;">Pay online via WeTravel (2.9% fee) or in-person at our Cusco office (cash: no fee; card: 3.9% fee) before the briefing</p>
            <p style="color: {color_texto}; font-size: 12px; margin: 5px 0;">Pay up to one day before the briefing.</p>
        </div>
        """

    contenido += f"""
        <div style="text-align: center; margin-top: 20px; padding-top: 10px; border-top: 1px solid #ccc;">
            <p style="color: {color_texto}; font-size: 12px;">Machu Picchu Reservations</p>
            <p style="color: {color_texto}; font-size: 12px;">Contact us: <a href="https://wa.me/51908851429" style="color: {color_tour};">+51 908 851 429</a> | Office: <a href="https://maps.app.goo.gl/XcfipVKjbuLeY3no9" style="color: {color_tour};">Portal Nuevo Nro 270, Cusco, Peru</a></p>
        </div>
    </div>
    """

    nombre_archivo = "confirmacion.html"
    with open(nombre_archivo, "w", encoding="utf-8") as file:
        file.write(f"""
        <html>
        <head>
            <title>Confirmación de Reserva</title>
            <style>
                body {{ font-family: 'Verdana', sans-serif; background-color: #f0f0f0; margin: 20px; }}
                p {{ line-height: 1.6; }}
                ul {{ list-style-type: none; padding-left: 0; }}
                ul li::before {{ content: "✔"; color: {color_tour}; font-weight: bold; display: inline-block; width: 1em; margin-left: -1em; }}
            </style>
        </head>
        <body>
            {contenido}
        </body>
        </html>
        """)
    print(f"Confirmación guardada como {nombre_archivo}")

def menu_principal():
    global ventana, nombre_var
    if ventana is None or not ventana.winfo_exists():
        ajustar_dpi()
        ventana = tk.Tk()
        ventana.title("MPR")
        ventana.geometry("350x550")  # Smaller window size
        ventana.iconbitmap(resource_path("logo_nuevo.ico"))
        ventana.resizable(False, False)
    else:
        limpiar_ventana(ventana)
        ventana.title("MPR")
        ventana.geometry("350x550")  # Restablece el tamaño cada vez que vuelvas al menú principal
        ventana.iconbitmap(resource_path("logo_nuevo.ico"))
        ventana.resizable(False, False)

    # Set a plain background color
    ventana.configure(bg="#f0f0f0")  # Light gray background

    # Create a frame to hold all content and center it vertically
    main_frame = tk.Frame(ventana, bg="#f0f0f0")
    main_frame.pack(expand=True)  # Center the frame vertically in the window

    # Title
    tk.Label(main_frame, text="PROGRAMA DE\nCONFIRMACIONES MODO EXTENSO", font=("Verdana", 10), fg="Purple", bg="#f0f0f0").pack(pady=10)

    # Buttons (stacked vertically and centered horizontally)
    tk.Button(main_frame, text="SALKANTAY", command=menu_salkantay, width=25, bg="#fff58e").pack(pady=10)
    tk.Button(main_frame, text="LLACTAPATA", command=lambda: seleccionar_transporte(Llactapata3DTrain, Llactapata3DCar), width=25, bg="#fff58e").pack(pady=10)
    tk.Button(main_frame, text="INCA TRAIL", command=menu_inca_trail, width=25, bg="#fff58e").pack(pady=10)
    tk.Button(main_frame, text="INKA JUNGLE", command=menu_inka_jungle, width=25, bg="#fff58e").pack(pady=10)
    tk.Button(main_frame, text="MACHU PICCHU", command=menu_machu_picchu, width=25, bg="#fff58e").pack(pady=10)
    tk.Button(main_frame, text="AMAZON MANU", command=menu_amazonas, width=25, bg="#fff58e").pack(pady=10)
    tk.Button(main_frame, text="CHOQUEQUIRAO", command=menu_choquequirao, width=25, bg="#fff58e").pack(pady=10)
    tk.Button(main_frame, text="TOURS DIARIOS", command=menu_tours_diarios, width=25, bg="#ee8eff").pack(pady=10)

    # Frame for bottom buttons
    frame_botones = tk.Frame(main_frame, bg="#f0f0f0")
    frame_botones.pack(pady=10)
    tk.Button(frame_botones, text="Ver ultima\nconfirmación", command=ver_confirmacion, width=15, bg="#c1ff8e").pack(side=tk.LEFT, padx=10)
    tk.Button(frame_botones, text="Regresar", command=pre_menu, width=10, bg="#ff8e8e").pack(side=tk.LEFT, padx=10)

    ventana.mainloop()

def ver_confirmacion():
    import os
    import webbrowser
    from tkinter import messagebox

    ruta_actual = os.path.dirname(os.path.abspath(sys.executable))
    archivo_confirmacion = os.path.join(ruta_actual, "confirmacion.html")

    if os.path.exists(archivo_confirmacion):
        webbrowser.open_new_tab(archivo_confirmacion)
    else:
        messagebox.showerror("Error", "No se encontró el archivo de confirmación.")

def seleccionar_transporte(tour_train, tour_car):
    limpiar_ventana(ventana)
    
    def seleccionar_by_train():
        ingresar_datos(tour_train)
    
    def seleccionar_by_car():
        ingresar_datos(tour_car)
    
    tk.Label(ventana, text="Selecciona el tipo de transporte:").pack(pady=25)
    
    tk.Button(ventana, text="BY TRAIN", command=seleccionar_by_train, width=25, bg="#fff58e").pack(pady=5)
    tk.Button(ventana, text="BY CAR", command=seleccionar_by_car, width=25, bg="#fff58e").pack(pady=5)
    
    tk.Button(ventana, text="Volver al menú principal", command=menu_principal, width=25, bg="#ff8e8e").pack(pady=20)

def menu_salkantay():
    limpiar_ventana(ventana)

    tk.Label(ventana, text="---- SALKANTAY -----").pack(pady=25)

    tk.Button(ventana, text="SALKANTAY 5D", command=lambda: seleccionar_transporte(Salkantay5DTrain, Salkantay5DCar), width=25, bg="#fff58e").pack(pady=5)
    tk.Button(ventana, text="SALKANTAY 4D", command=lambda: seleccionar_transporte(Salkantay4DTrain, Salkantay4DCar), width=25, bg="#fff58e").pack(pady=5)
    tk.Button(ventana, text="SALKANTAY 3D", command=lambda: seleccionar_transporte(Salkantay3DTrain, Salkantay3DCar), width=25, bg="#fff58e").pack(pady=5)
    tk.Button(ventana, text="SALKANTAY 2D", command=lambda: ingresar_datos(Salkantay2D), width=25, bg="#fff58e").pack(pady=5)  # Sin selección de transporte
    tk.Button(ventana, text="Volver al menú principal", command=menu_principal, width=25, bg="#ff8e8e").pack(pady=20)

def menu_inca_trail():
    limpiar_ventana(ventana)

    tk.Label(ventana, text="---- INCA TRAIL -----").pack(pady=25)

    tk.Button(ventana, text="INCA TRAIL 4D", command=lambda: ingresar_datos(IncaTrail4D), width=25, bg="#fff58e").pack(pady=5)
    tk.Button(ventana, text="INCA TRAIL 2D", command=lambda: ingresar_datos(IncaTrail2D), width=25, bg="#fff58e").pack(pady=5)
    tk.Button(ventana, text="INCA TRAIL 1D", command=lambda: ingresar_datos(IncaTrail1D), width=25, bg="#fff58e").pack(pady=5)
    tk.Button(ventana, text="Volver al menú principal", command=menu_principal, width=25, bg="#ff8e8e").pack(pady=20)

def menu_inka_jungle():
    limpiar_ventana(ventana)

    tk.Label(ventana, text="---- INKA JUNGLE -----").pack(pady=25)

    tk.Button(ventana, text="INKA JUNGLE 4D", command=lambda: seleccionar_transporte(IncaJungle4DTrain, IncaJungle4DCar), width=25, bg="#fff58e").pack(pady=5)
    tk.Button(ventana, text="INKA JUNGLE 3D", command=lambda: seleccionar_transporte(IncaJungle3DTrain, IncaJungle3DCar), width=25, bg="#fff58e").pack(pady=5)
    tk.Button(ventana, text="Volver al menú principal", command=menu_principal, width=25, bg="#ff8e8e").pack(pady=20)

def menu_machu_picchu():
    limpiar_ventana(ventana)

    tk.Label(ventana, text="---- MACHU PICCHU -----").pack(pady=25)

    tk.Button(ventana, text="MAPI FULL DAY", command=lambda: ingresar_datos(MachuPicchuFullDay), width=25, bg="#fff58e").pack(pady=5)
    tk.Button(ventana, text="MAPI 2D TRAIN", command=lambda: ingresar_datos(MachuPicchu2DTrain), width=25, bg="#fff58e").pack(pady=5)
    tk.Button(ventana, text="VALLE + MAPI", command=lambda: ingresar_datos(SacredValleyMachuPicchu2D), width=25, bg="#fff58e").pack(pady=5)
    tk.Button(ventana, text="MAPI 2D CAR", command=lambda: ingresar_datos(MachuPicchuByCar2D), width=25, bg="#fff58e").pack(pady=5)
    tk.Button(ventana, text="MAPI BY CAR + BY TRAIN 2D", command=lambda: ingresar_datos(MachuPicchuByCarTrain2D), width=25, bg="#fff58e").pack(pady=5)
    tk.Button(ventana, text="MAPI BY CAR 3D", command=lambda: ingresar_datos(MachuPicchuByCar3D), width=25, bg="#fff58e").pack(pady=5)
    tk.Button(ventana, text="CITY + VALLE-MAPI 3D", command=lambda: ingresar_datos(CuscoCitySacredValleyMachuPicchu3D), width=25, bg="#fff58e").pack(pady=5)  # Nueva opción
    tk.Button(ventana, text="Volver al menú principal", command=menu_principal, width=25, bg="#ff8e8e").pack(pady=20)

def menu_amazonas():
    limpiar_ventana(ventana)

    tk.Label(ventana, text="---- AMAZONAS -----").pack(pady=25)

    tk.Button(ventana, text="AMAZON 4D-3N", command=lambda: ingresar_datos(AmazonTour4D), width=25, bg="#fff58e").pack(pady=5)
    tk.Button(ventana, text="AMAZON 3D-2N", command=lambda: ingresar_datos(AmazonTour3D), width=25, bg="#fff58e").pack(pady=5)
    tk.Button(ventana, text="Volver al menú principal", command=menu_principal, width=25, bg="#ff8e8e").pack(pady=20)

def menu_choquequirao():
    limpiar_ventana(ventana)

    tk.Label(ventana, text="---- CHOQUEQUIRAO -----").pack(pady=25)

    tk.Button(ventana, text="CHOQUE 4D-3N", command=lambda: ingresar_datos(Choquequirao4Days), width=25, bg="#fff58e").pack(pady=5)
    tk.Button(ventana, text="CHOQUE 3D-2N (PRUEBA)", command=lambda: ingresar_datos(Choquequirao3Days), width=25, bg="#fff58e").pack(pady=5)
    tk.Button(ventana, text="Volver al menú principal", command=menu_principal, width=25, bg="#ff8e8e").pack(pady=20)

def menu_tours_diarios():
    limpiar_ventana(ventana)

    tk.Label(ventana, text="---- TOURS DIARIOS -----").pack(pady=25)

    tk.Button(ventana, text="VALLE VIP", command=lambda: ingresar_datos(ValleSagradoFullDayTour), width=25, bg="#ee8eff").pack(pady=5)
    tk.Button(ventana, text="RAINBOW MOUNTAIN", command=lambda: ingresar_datos(RainbowMountainFullDayTour), width=25, bg="#ee8eff").pack(pady=5)
    tk.Button(ventana, text="HUMANTAY LAKE", command=lambda: ingresar_datos(HumantayLakeFullDayTour), width=25, bg="#ee8eff").pack(pady=5)
    tk.Button(ventana, text="PALCOYO MOUNTAIN", command=lambda: ingresar_datos(PalcoyoFullDayTour), width=25, bg="#ee8eff").pack(pady=5)
    tk.Button(ventana, text="MARAS MORAY", command=lambda: ingresar_datos(MorayFullDayTour), width=25, bg="#ee8eff").pack(pady=5)
    tk.Button(ventana, text="CITY TOUR", command=lambda: ingresar_datos(CuscoCityTour), width=25, bg="#ee8eff").pack(pady=5)
    tk.Button(ventana, text="AUSANGATE 7LAKES", command=lambda: ingresar_datos(AusangateFullDayTour), width=25, bg="#ee8eff").pack(pady=5)
    tk.Button(ventana, text="Volver al menú principal", command=menu_principal, width=25, bg="#ff8e8e").pack(pady=20)

def formatear_numero(entry):
    numero = entry.get().strip()
    numero = re.sub(r'[^\d+]', '', numero)
    numero = re.sub(r'\s+', '', numero)
    if not numero.startswith('+'):
        numero = '+' + numero
    
    numero = re.sub(r'^\+0+', '+', numero)
    entry.delete(0, tk.END)
    entry.insert(0, numero)

def incrementar_fecha(fecha):
    current_date = datetime.strptime(fecha.get(), '%d/%m/%Y')
    new_date = current_date + timedelta(days=1)
    fecha.set(new_date.strftime('%d/%m/%Y'))

def decrementar_fecha(fecha):
    current_date = datetime.strptime(fecha.get(), '%d/%m/%Y')
    # Verifica que la nueva fecha no sea menor que mañana
    tomorrow = datetime.now() + timedelta(days=1)
    if current_date > tomorrow:
        new_date = current_date - timedelta(days=1)
        fecha.set(new_date.strftime('%d/%m/%Y'))

def cambiar_fecha_con_mouse(event, fecha_var):
    if event.delta > 0:  # Rueda hacia arriba (Windows)
        incrementar_fecha(fecha_var)
    else:  # Rueda hacia abajo (Windows)
        decrementar_fecha(fecha_var)

def cambiar_fecha_con_mouse_linux(event, fecha_var):
    if event.num == 4:  # Scroll hacia arriba (Linux)
        incrementar_fecha(fecha_var)
    elif event.num == 5:  # Scroll hacia abajo (Linux)
        decrementar_fecha(fecha_var)

ubicacion = "https://maps.app.goo.gl/HZZu2vWW5FnWF3Gz5"

detalles_tours = {
    "SALKANTAY 5D": {"nombre_completo": "SALKANTAY TREK 5 DAYS TO MACHU PICCHU AND LLACTAPATA TREK", "hora_briefing": "7:00 pm", "lugar_encuentro": ubicacion},
    "SALKANTAY 4D": {"nombre_completo": "SALKANTAY TREK 4 DAYS TO MACHU PICCHU", "hora_briefing": "7:00 pm", "lugar_encuentro": ubicacion},
    "SALKANTAY 3D": {"nombre_completo": "SALKANTAY TREK 3 DAYS TO MACHU PICCHU", "hora_briefing": "7:00 pm", "lugar_encuentro": ubicacion},
    "SALKANTAY 2D": {"nombre_completo": "SALKANTAY PASS AND HUMANTAY LAKE HIKE 2 DAYS", "hora_briefing": "7:00 pm", "lugar_encuentro": ubicacion},
    "LLACTAPATA": {"nombre_completo": "LLACTAPATA TREK TO MACHU PICCHU 3D 2N", "hora_briefing": "7:00 pm", "lugar_encuentro": ubicacion},
    "INCA TRAIL": {"nombre_completo": "INCA TRAIL TREK TO MACHU PICCHU", "hora_briefing": "6:00 pm", "lugar_encuentro": ubicacion},
    "INCA JUNGLE": {"nombre_completo": "INCA JUNGLE TRAIL TO MACHU PICCHU", "hora_briefing": "6:00 pm", "lugar_encuentro": ubicacion},
    "AMAZON MANU": {"nombre_completo": "AMAZON TOUR MANU CULTURAL ZONE", "hora_briefing": "6:00 pm", "lugar_encuentro": ubicacion},
    "CHOQUEQUIRAO": {"nombre_completo": "CHOQUEQUIRAO TREK", "hora_briefing": "6:00 pm", "lugar_encuentro": ubicacion},
    
    "MAPI FULL DAY": {"nombre_completo": "MACHU PICCHU TOUR FULL DAY BY TRAIN", "hora_briefing": "0:00 pm", "lugar_encuentro": ubicacion},
    "MAPI 2D TRAIN": {"nombre_completo": "MACHU PICCHU TOUR 2 DAYS BY TRAIN", "hora_briefing": "0:00 pm", "lugar_encuentro": ubicacion},
    "VALLE + MAPI": {"nombre_completo": "SACRED VALLEY AND MACHU PICCHU 2 DAYS TOUR", "hora_briefing": "0:00 pm", "lugar_encuentro": ubicacion},
    "MAPI 2D CAR": {"nombre_completo": "MACHU PICCHU TOUR BY CAR 2D 1N", "hora_briefing": "0:00 pm", "lugar_encuentro": ubicacion},
    "MAPI 2D CAR TRAIN": {"nombre_completo": "MACHU PICCHU TOUR BY CAR AND BY TRAIN 2D 1N", "hora_briefing": "0:00 pm", "lugar_encuentro": ubicacion},
    "MAPI 3D CAR": {"nombre_completo": "MACHU PICCHU TOUR BY BUS 3D 2N", "hora_briefing": "0:00 pm", "lugar_encuentro": ubicacion},
    
    "VALLE VIP": {"nombre_completo":"SACRED VALLEY TOUR FULL DAY"},
    "MONTAÑA": {"nombre_completo":"RAINBOW MOUNTAIN AND RED VALLEY FULL DAY"},
    "HUMANTAY": {"nombre_completo":"HUMANTAY LAKE HIKE FULL DAY"},
    "PALCOYO": {"nombre_completo":"PALCOYO MOUNTAIN FULL DAY "},
    "MARAS MORAY": {"nombre_completo":"MORAY AND SALT MINES DAY TOUR"},
    "CITY TOUR": {"nombre_completo":"CUSCO CITY TOUR"},
    "7 LAGUNAS": {"nombre_completo":"AUSANGATE FULL DAY TOUR 7 LAKES"}
}

def cargar_mensaje_guardado():
    try:
        with open(ruta_mensaje, "r", encoding="utf-8") as archivo:
            return archivo.read()
    except FileNotFoundError:
        return mensaje_en2_predeterminado
    
def guardar_mensaje(ventana_mensaje):
    global mensaje_en2
    mensaje_en2 = text_box_editar_mensaje.get("1.0", tk.END).strip()
    try:
        with open(ruta_mensaje, "w", encoding="utf-8") as archivo:
            archivo.write(mensaje_en2)
        ventana_mensaje.destroy()
        print("Mensaje guardado correctamente.")
    except Exception as e:
        print(f"Error al guardar el mensaje: {e}")

def formatear_nombres_y_numeros(nombres_text, numeros_text):
    # Formatear nombres y números, eliminando los que no tienen número
    nombres_formateados = []
    numeros_formateados = []

    # Dividimos las líneas de nombres y números
    nombres_lineas = nombres_text.strip().splitlines()
    numeros_lineas = numeros_text.strip().splitlines()

    for nombre, numero in zip(nombres_lineas, numeros_lineas):
        nombre = nombre.strip().lower().title()  # Formatear el nombre en tipo oración
        numero = re.sub(r'[^\d+]', '', numero)  # Quitar caracteres no numéricos, excepto +

        # Si el número no está vacío, formatear y guardar
        if numero:
            # Si el número comienza con '+', asegurarse de que solo haya uno
            if numero.startswith('+'):
                numero = '+' + re.sub(r'\++', '', numero[1:])  # Eliminar "+" adicionales
            elif numero.startswith('00'):
                numero = '+' + numero[2:]  # Convertir "00" al formato "+"
            elif not numero.startswith('+'):
                numero = '+' + numero

            nombres_formateados.append(nombre)  # Solo añadir si hay número
            numeros_formateados.append(numero)

    return nombres_formateados, numeros_formateados

def formatear_nombres_y_numeros_callback():
    nombres_text = text_box_nombres.get("1.0", tk.END)
    numeros_text = text_box_numeros.get("1.0", tk.END)

    nombres_formateados, numeros_formateados = formatear_nombres_y_numeros(nombres_text, numeros_text)

    # Mostrar los nombres y números formateados en las cajas de texto
    text_box_nombres.delete("1.0", tk.END)
    text_box_nombres.insert(tk.END, "\n".join(nombres_formateados))

    text_box_numeros.delete("1.0", tk.END)
    text_box_numeros.insert(tk.END, "\n".join(numeros_formateados))

def enviar_recordatorio():
    global combobox_tour, entry_fecha, combobox_briefing, text_box_nombres, text_box_numeros, stored_messages, store_messages_var, ubicacion

    try:
        # Verificar si se ha seleccionado un tour
        tour = combobox_tour.get()
        if not tour:
            tk.messagebox.showwarning("Error", "Por favor, selecciona un tour antes de enviar el recordatorio.")
            return

        # Verificar si se han formateado los nombres y números
        nombres = text_box_nombres.get("1.0", tk.END).strip().split('\n')
        numeros = text_box_numeros.get("1.0", tk.END).strip().split('\n')

        # Verificar si los nombres están formateados correctamente (capitalizados)
        if not all(nombre.istitle() for nombre in nombres if nombre.strip()):
            tk.messagebox.showwarning("Error", "Los nombres no están formateados. Por favor, vuelva a formatear.")
            return

        # Verificar si todos los números tienen el prefijo '+' al inicio
        if not all(numero.startswith('+') for numero in numeros if numero.strip()):
            tk.messagebox.showwarning("Error", "Por favor, asegúrate de que todos los números de teléfono comiencen con '+'.")
            return

        # Verificar si los números de teléfono están formateados correctamente
        if not all(re.match(r'^\+?\d{10,15}$', numero) for numero in numeros if numero.strip()):
            tk.messagebox.showwarning("Error", "Por favor, formatea todos los números de teléfono antes de enviar el recordatorio.")
            return

        # Verificar que la cantidad de nombres y números coincida
        if len(nombres) != len(numeros):
            tk.messagebox.showwarning("Error", "La cantidad de nombres y números de teléfono no coinciden. Vuelva a formatear.")
            return

        # Obtener la fecha del tour
        fecha_tour = entry_fecha.get()
        try:
            dia, mes, año = map(int, fecha_tour.split('/'))
        except ValueError:
            tk.messagebox.showwarning("Error", "El formato de la fecha es incorrecto. Usa DD/MM/AAAA.")
            return

        # Obtener detalles del tour
        detalles = detalles_tours.get(tour, {})
        hora_briefing = detalles.get("hora_briefing")
        nombre_completo_tour = detalles.get("nombre_completo", tour)

        # Verificar si el tour requiere una hora de briefing específica
        briefing_custom = combobox_briefing.get().strip()
        if "hora_briefing" in detalles and detalles["hora_briefing"] != "0:00 pm":
            if not briefing_custom:
                # Si no se ha ingresado una hora personalizada, solicitar confirmación
                confirmacion = tk.messagebox.askyesno(
                    "Hora de Briefing",
                    f"No se ha ingresado una hora de briefing. ¿Desea enviar en el horario por defecto {hora_briefing}?"
                )
                if not confirmacion:
                    return
            else:
                hora_briefing = briefing_custom  # Usar la hora personalizada

        fecha_tour_formateada_en = fecha_nombre(dia, mes, año)
        fecha_briefing = (datetime(año, mes, dia) - timedelta(days=1)).strftime('%A, %d %B %Y')

        # Mensaje base del recordatorio en inglés
        for nombre, numero in zip(nombres, numeros):
            if numero:
                if "hora_briefing" in detalles and detalles["hora_briefing"] != "0:00 pm":  # Tours con briefing
                    mensaje_base = (
                        f"*Hello {nombre}*,\n\n"
                        f"This is a reminder of your upcoming tour with us {nombre_completo_tour}.\n\n"
                        f"📅 *Tour Date*: {fecha_tour_formateada_en}\n"
                        f"📅 *Briefing Date*: {fecha_briefing} at {hora_briefing}\n"
                        f"📍 *Office Location*: {ubicacion} \n"
                        f"Remember: if you have a balance, please pay it before your briefing session.\n\n"
                        f"{mensaje_en2}"
                    )
                elif detalles.get("hora_briefing") == "0:00 pm":  # Tours MAPI sin briefing
                    mensaje_base = (
                        f"Hello {nombre},\n\n"
                        f"This is a reminder of your upcoming tour with us {nombre_completo_tour}.\n\n"
                        f"📅 *Tour Date*: {fecha_tour_formateada_en}\n"
                        f"📅 *Briefing Date*: {fecha_briefing}\n"
                        f"📍 *Office Location*: {ubicacion} \n"
                        f"Note: You can come to the office anytime between 7:00 am and 10:00 pm on the day of your briefing to pick up your tickets.\n\n"
                        f"{mensaje_en2}"
                    )
                else:  # Tours Full Day sin briefing
                    mensaje_base = (
                        f"Hello {nombre},\n\n"
                        f"This is a reminder of your upcoming tour with us {nombre_completo_tour}.\n\n"
                        f"📅 *Tour Date*: {fecha_tour_formateada_en}\n"
                        f"📍 *Office Location*: {ubicacion} \n\n"
                        f"{mensaje_en2}"
                    )

                # Almacenar o enviar el mensaje
                if store_messages_var.get():  # Si el checkbox está seleccionado, almacenar los mensajes
                    stored_messages.append((numero, mensaje_base))
                else:
                    try:
                        kit.sendwhatmsg_instantly(numero, mensaje_base, 15, True, 2)
                    except Exception as e:
                        print(f"Error al enviar mensaje a {numero}: {e}")

        # Limpiar los cuadros de texto después de enviar o almacenar mensajes
        text_box_nombres.delete("1.0", tk.END)
        text_box_numeros.delete("1.0", tk.END)

        if store_messages_var.get():
            print("Mensajes almacenados con éxito.")
        else:
            print("Mensajes enviados con éxito.")

    except Exception as e:
        print(f"Error en enviar_recordatorio: {e}")

def obtener_fecha_actual():
    tomorrow = datetime.now() + timedelta(days=1)
    return tk.StringVar(value=tomorrow.strftime('%d/%m/%Y'))

def ver_mensaje():
    ventana_mensaje = tk.Toplevel(ventana)
    ventana_mensaje.title("Editar mensaje")
    ventana_mensaje.resizable(False,False)

    tk.Label(ventana_mensaje, text="Edita el mensaje de recordatorio:").pack(pady=5)

    global text_box_editar_mensaje
    text_box_editar_mensaje = tk.Text(ventana_mensaje, height=15, width=60)
    text_box_editar_mensaje.pack(pady=10)
    
    # Cargar el mensaje guardado en el text_box
    text_box_editar_mensaje.insert(tk.END, cargar_mensaje_guardado())

    # Botón para guardar los cambios
    guardar_btn = tk.Button(ventana_mensaje, text="Guardar", command=lambda: guardar_mensaje(ventana_mensaje), bg="#c1ff8e")
    guardar_btn.pack(pady=5)

def actualizar_estado_briefing(event=None):
    tour = combobox_tour.get()
    detalles = detalles_tours.get(tour, {})
    hora_briefing = detalles.get("hora_briefing")

    if hora_briefing == "0:00 pm" or tour not in detalles_tours:
        combobox_briefing.config(state="disabled")
        combobox_briefing.set('')  # Limpiar el valor de la hora de briefing
    else:
        combobox_briefing.config(state="normal")

def incrementar_fecha(fecha):
    current_date = datetime.strptime(fecha.get(), '%d/%m/%Y')
    new_date = current_date + timedelta(days=1)
    fecha.set(new_date.strftime('%d/%m/%Y'))

def decrementar_fecha(fecha):
    current_date = datetime.strptime(fecha.get(), '%d/%m/%Y')
    # Verifica que la nueva fecha no sea menor que mañana
    tomorrow = datetime.now() + timedelta(days=1)
    if current_date > tomorrow:
        new_date = current_date - timedelta(days=1)
        fecha.set(new_date.strftime('%d/%m/%Y'))

def cambiar_fecha_con_mouse(event, fecha_var):
    if event.delta > 0:  # Rueda hacia arriba (Windows)
        incrementar_fecha(fecha_var)
    else:  # Rueda hacia abajo (Windows)
        decrementar_fecha(fecha_var)

def cambiar_fecha_con_mouse_linux(event, fecha_var):
    if event.num == 4:  # Scroll hacia arriba (Linux)
        incrementar_fecha(fecha_var)
    elif event.num == 5:  # Scroll hacia abajo (Linux)
        decrementar_fecha(fecha_var)

def recordatorio():
    global text_box_nombres, text_box_numeros, entry_fecha, combobox_tour, store_messages_var, combobox_briefing

    # Inicializar la variable si aún no se ha hecho
    store_messages_var = tk.BooleanVar()

    limpiar_ventana(ventana)  
    
    ventana.title("Recordatorios V1")
    ventana.geometry("700x680")
    ventana.resizable(False, False)
    ventana.iconbitmap(resource_path("calendario.ico"))

    tours = [
        "SALKANTAY 5D", "SALKANTAY 4D", "SALKANTAY 3D", "SALKANTAY 2D",
        "LLACTAPATA", "INCA TRAIL", "INCA JUNGLE", "MAPI FULL DAY",
        "MAPI 2D TRAIN", "VALLE + MAPI", "MAPI 2D CAR", "MAPI 2D CAR TRAIN",
        "MAPI 3D CAR", "AMAZON MANU", "CHOQUEQUIRAO", "VALLE VIP", "MONTAÑA",
        "HUMANTAY", "PALCOYO", "MARAS MORAY", "CITY TOUR", "7 LAGUNAS"
    ]

    # Opciones para la hora del Briefing
    horas_briefing = [
        "4:00 - 5:00 pm",
        "5:00 - 6:00 pm",
        "6:00 - 7:00 pm",
        "7:00 - 8:00 pm",
        "8:00 - 9:00 pm"
    ]

    # Crear un Frame para alinear los widgets en horizontal
    frame_horizontal = tk.Frame(ventana)
    frame_horizontal.pack(pady=10)

    # Elemento Tour (ComboBox)
    tk.Label(frame_horizontal, text="TOUR").grid(row=0, column=0, padx=10)
    nombres_tour = tk.StringVar()
    combobox_tour = ttk.Combobox(frame_horizontal, textvariable=nombres_tour, values=tours, state="readonly", width=20)
    combobox_tour.grid(row=1, column=0, padx=10)

    # Elemento Fecha del Tour
    tk.Label(frame_horizontal, text="INICIO DEL TOUR").grid(row=0, column=1, padx=10)
    fecha_var = obtener_fecha_actual()
    entry_fecha = tk.Entry(frame_horizontal, textvariable=fecha_var, font=('Arial', 12), width=15, state="readonly", justify='center')
    entry_fecha.grid(row=1, column=1, padx=10)

    # Asociar la rueda del mouse a las funciones de incremento y decremento
    entry_fecha.bind("<MouseWheel>", lambda event: cambiar_fecha_con_mouse(event, fecha_var))  # Windows
    entry_fecha.bind("<Button-4>", lambda event: cambiar_fecha_con_mouse_linux(event, fecha_var))  # Linux scroll up
    entry_fecha.bind("<Button-5>", lambda event: cambiar_fecha_con_mouse_linux(event, fecha_var))  # Linux scroll down

    # Elemento Hora del Briefing (ComboBox)
    tk.Label(frame_horizontal, text="Hora del Briefing").grid(row=0, column=2, padx=10)
    hora_briefing_var = tk.StringVar()
    combobox_briefing = ttk.Combobox(frame_horizontal, textvariable=hora_briefing_var, values=horas_briefing, state="readonly", width=20)
    combobox_briefing.grid(row=1, column=2, padx=10)

    # Crear un frame para contener las dos columnas
    columnas_frame = tk.Frame(ventana)
    columnas_frame.pack(pady=10)

    # Text Box para los Nombres
    tk.Label(columnas_frame, text="Nombres").grid(row=0, column=0, padx=10)
    text_box_nombres = tk.Text(columnas_frame, height=20, width=32)
    text_box_nombres.grid(row=1, column=0, padx=10)

    # Text Box para los Números
    tk.Label(columnas_frame, text="Números").grid(row=0, column=1, padx=10)
    text_box_numeros = tk.Text(columnas_frame, height=20, width=32)
    text_box_numeros.grid(row=1, column=1, padx=10)

    # Checkbox para almacenar mensajes
    store_messages_var.set(False)  # Asegúrate de que esté correctamente inicializado
    checkbox_store = tk.Checkbutton(ventana, text="Almacenar mensajes", variable=store_messages_var)
    checkbox_store.pack(pady=5)

    button_frame = tk.Frame(ventana)
    button_frame.pack(pady=10)

    formatear_btn = tk.Button(button_frame, text="Formatear", command=formatear_nombres_y_numeros_callback, width=10, bg="#8ebbff")
    formatear_btn.pack(side=tk.LEFT, padx=5)

    enviar_btn = tk.Button(button_frame, text="Enviar", command=enviar_recordatorio, width=10, bg="#c1ff8e")
    enviar_btn.pack(side=tk.LEFT, padx=5)

    editar_mensaje_btn = tk.Button(button_frame, text="Editar", command=ver_mensaje, width=10, bg="#fff58e")
    editar_mensaje_btn.pack(side=tk.LEFT, padx=5)

    salir_btn = tk.Button(button_frame, text="Regresar", command=pre_menu, width=10, bg="#ff8e8e")
    salir_btn.pack(side=tk.LEFT, padx=5)

    tk.Label(ventana, text="Los tours como son MapiFull Day, MapiByTrain2D,\nMapiByCar2D, MapiByCarByTrain2D, MapiByCar3D\ny Valle+Mapi2D no tienen horario específico de briefing", fg="Red", font=("Verdana", 8)).pack(pady=1)

ventana = None
mensajes_whatsapp = []

nombres_tours = {
    Salkantay5DTrain: "SALKANTAY TREK 5 DAYS TO MACHU PICCHU",
    Salkantay4DTrain: "SALKANTAY TREK 4 DAYS TO MACHU PICCHU",
    Salkantay3DTrain: "SALKANTAY TREK 3 DAYS TO MACHU PICCHU",
    Salkantay2D: "SALKANTAY PASS + HUMANTAY LAKE 2 DAY HIKE",
    Salkantay5DCar: "SALKANTAY TREK 5 DAYS TO MACHU PICCHU",
    Salkantay4DCar: "SALKANTAY TREK 4 DAYS TO MACHU PICCHU",
    Salkantay3DCar: "SALKANTAY TREK 3 DAYS TO MACHU PICCHU",
    Llactapata3DTrain: "LLACTAPATA TREK 3 DAYS TO MACHU PICCHU",
    Llactapata3DCar: "LLACTAPATA TREK 3 DAYS TO MACHU PICCHU",
    IncaTrail4D: "INCA TRAIL TO MACHU PICCHU 4 DAYS",
    IncaTrail2D: "INCA TRAIL TO MACHU PICCHU 2 DAYS",
    IncaTrail1D: "INCA TRAIL TO MACHU PICCHU 1 DAY",
    IncaJungle4DTrain: "INCA JUNGLE TRAIL 4D-3N",
    IncaJungle3DTrain: "INCA JUNGLE TRAIL 3D-2N",
    IncaJungle4DCar: "INCA JUNGLE TRAIL 4D-3N",
    IncaJungle3DCar: "INCA JUNGLE TRAIL 3D-2N",
    MachuPicchuFullDay: "MACHU PICCHU TOUR BY TRAIN - 1 DAY",
    MachuPicchu2DTrain: "MACHU PICCHU TOUR BY TRAIN - 2 DAYS",
    SacredValleyMachuPicchu2D: "SACRED VALLEY + MACHU PICCHU TOUR - 2 DAYS",
    MachuPicchuByCar2D: "MACHU PICCHU TOUR BY CAR - 2 DAYS",
    MachuPicchuByCarTrain2D: "MACHU PICCHU BY CAR & TRAIN - 2 DAYS",
    MachuPicchuByCar3D: "MACHU PICCHU TOUR BY CAR - 3 DAYS",
    AmazonTour4D: "AMAZON TOUR MANU CULTURAL 4D - 3N",
    AmazonTour3D: "AMAZON TOUR MANU CULTURAL 3D - 2N",
    Choquequirao4Days: "CHOQUEQUIRAO TREK 4D - 3N",
    Choquequirao3Days: "CHOQUEQUIRAO TREK 3D - 2N",
    HumantayLakeFullDayTour: "HUMANTAY LAKE HIKE FULL DAY",
    RainbowMountainFullDayTour: "RAINBOW MOUNTAIN + RED VALLEY FULL DAY",
    PalcoyoFullDayTour: "PALCOYO MOUNTAIN FULL DAY",
    ValleSagradoFullDayTour: "SACRED VALLEY TOUR FULL DAY",
    MorayFullDayTour: "MORAY + SALT MINES DAY TOUR",
    CuscoCityTour: "CUSCO CITY TOUR",
    AusangateFullDayTour: "AUSANGATE FULL DAY TOUR - 7 LAKES",
}

ruta_mensaje = os.path.join(tempfile.gettempdir(), "mensaje_en2.txt")

mensaje_en2_predeterminado = (
    "Machu Picchu Reservations"
)

ruta_mensaje = os.path.join(tempfile.gettempdir(), "mensaje_en2.txt")

mensaje_en2 = cargar_mensaje_guardado()

stored_messages = []

def resource_path(relative_path):
    """Obtiene la ruta absoluta del recurso, compatible tanto con PyInstaller como en desarrollo"""
    try:
        # PyInstaller almacena archivos temporales en _MEIPASS
        base_path = sys._MEIPASS
    except AttributeError:
        # Si estamos en desarrollo, usamos la ruta relativa normal
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

ajustar_dpi()

#pre_menu()