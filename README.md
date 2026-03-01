# GitHub Webhook Event Tracker

## 📌 Project Overview

This project implements a GitHub webhook integration using Flask and MongoDB.

It tracks repository activity (Push, Pull Request, and Merge events) and displays the latest activity on a simple web interface that updates every 15 seconds.

---

## ⚙️ Tech Stack

- Python (Flask)
- MongoDB (Atlas)
- GitHub Webhooks
- JavaScript (Frontend polling)
- HTML (Minimal UI)

---

## 🏗 System Architecture

GitHub Repository (action-repo)
        ↓
Webhook (HTTP POST request)
        ↓
Flask Backend (/webhook endpoint)
        ↓
MongoDB (stores minimal event data)
        ↓
Frontend Polling (/events every 15 seconds)
        ↓
UI Updates Automatically

---

