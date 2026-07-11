# 🧠 MeetMind — The AI-Powered Meeting Secretary

> **MeetMind** is a full-stack Python application that transforms messy meeting notes into structured, trackable action items. It automatically extracts tasks, assigns team members, detects due dates, stores everything in the cloud, and sends proactive reminders—all without requiring the user to write perfectly formatted notes.

---

## 📋 Project Overview

| **Category** | **Details** |
| :--- | :--- |
| **Project Name** | MeetMind |
| **Domain** | Productivity & Task Automation |
| **Type** | Full-stack Web Application + REST API |
| **Status** | ✅ **Production-Ready Prototype** |

In today's fast-paced world, meeting notes are often written haphazardly: *"meeting with siddhi on tuesday"*, *"Project submission - 7 July"*, *"cation - fix the server"*. MeetMind understands these messy, real-world sentences and converts them into structured data.

---

## ✨ Key Features (What It Actually Does)

| # | Feature | How It Works |
| :--- | :--- | :--- |
| 1 | **Messy Text Upload** | Django web form accepts raw text or file uploads. |
| 2 | **Smart Task Extraction** | Uses Regex + Keyword Detection to find tasks. Does **not** require "Action:"—it detects bullet points, action verbs, names, and dates naturally. |
| 3 | **Auto-Assignment** | Scans the entire sentence for known team members (Alice, Bob, Siddhi, etc.) and assigns the task to them. |
| 4 | **Date Intelligence** | Parses relative dates like "tomorrow", "tuesday", "7 July" and converts them to `YYYY-MM-DD`. |
| 5 | **Cloud Storage** | Saves all meetings and action items to MongoDB Atlas (cloud database). |
| 6 | **Background Reminders** | A separate background thread (multithreading) checks for pending/overdue tasks every 10 seconds and prints reminders to the console. |
| 7 | **REST API (DRF)** | Exposes JSON endpoints (`/api/pending/`, `/api/meetings/`) for Slack or third-party integrations. |
| 8 | **CSV Export** | Exports all action items to a `.csv` file that opens directly in Excel. |
| 9 | **Meeting Dashboard** | Lists all stored meetings with links to view individual notes and tasks. |

---

## 🏗️ Architecture & Task Breakdown

The project strictly follows the **9-Step Task List** defined at the start. Here is the exact mapping between the tasks and the codebase:

| Step | Task Description | Implemented In | Status |
| :--- | :--- | :--- | :--- |
| **1** | Build Django form to paste or upload notes | `webapp/forms.py`, `webapp/views.py` | ✅ |
| **2** | Use regex to extract action items, `@name`, due dates | `extractor.py` (`extract_action_items`) | ✅ |
| **3** | Auto-assign action items to team members by name mention | `extractor.py` (scans `TEAM_MEMBERS` list) | ✅ |
| **4** | Store meetings and action items in MongoDB | `database.py` (`MongoDBHandler.save_meeting`) | ✅ |
| **5** | Track action item completion status | `models.py` (`ActionItem.is_completed`) | ✅ |
| **6** | Use multithreading for bulk notes processing | `reminder.py` & `main.py` | ✅ |
| **7** | Send pending action item reminders using threading | `reminder.py` (background while-loop) | ✅ |
| **8** | Build DRF API for Slack/Teams integration | `webapp/api_views.py` & `serializers.py` | ✅ |
| **9** | Export action items as CSV | `webapp/views.py` (`export_csv`) & `export.py` | ✅ |

---

## 📁 Project Folder Structure

Here is the exact file structure of the project. Every file has a specific purpose.
