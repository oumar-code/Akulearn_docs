# Data and Cybersecurity Fundamentals

**Computer Science | SS1 | Unit 1: Data and Cybersecurity Fundamentals**

---

## Lesson Information

- **Duration**: 90 minutes
- **Estimated Pages**: 13
- **NERDC Code**: CS.SS1.3.1-3.3
- **NERDC Description**: Data organization, databases, networks, cybersecurity essentials
- **WAEC Topic**: Data Representation and Security (8%)
- **Learning Level**: Foundational

## Learning Objectives

By the end of this lesson, you will be able to:

1. Differentiate data vs information and describe data quality attributes
2. Explain how data is organized (files, tables, records, fields) and basic database ideas
3. Describe network basics (LAN, WAN, internet) and data transmission concepts
4. Identify common cybersecurity threats and simple protective measures
5. Apply safe practices relevant to schools, cybercafes, and mobile banking in Nigeria

## Prerequisites

Before starting this lesson, ensure you understand:

- Understanding of input/output devices
- Basic algorithmic thinking
- Awareness of common digital tools (browsers, mobile apps)

## Content


### 3.1: Data vs Information and Data Organization

*Duration: 22 minutes*

**Data**: raw facts; **Information**: processed, meaningful output. Data quality: accuracy, completeness, timeliness, consistency. Organization: character → field → record → file → database. Tables hold rows (records) and columns (fields). Examples: student records, exam scores.


### 3.2: Databases and File Systems

*Duration: 22 minutes*

File storage vs databases (DBMS) for structured queries and multi-user access. Common DBMS: MySQL, PostgreSQL, SQLite. Key terms: primary key, query, table, form, report. Backup importance—use external drives or cloud when available.


### 3.3: Networks and Data Transmission Basics

*Duration: 23 minutes*

**LAN** (school network), **WAN**, **Internet**. Devices: router, switch, modem, access point. Transmission: wired (Ethernet), wireless (Wi-Fi). IP address identifies devices; bandwidth affects speed; latency affects responsiveness. Nigerian context: mixed reliability; mobile broadband common.


### 3.4: Cybersecurity Essentials

*Duration: 23 minutes*

Threats: malware (virus, worm, ransomware), phishing (fake emails/SMS), password attacks, unauthorized access, USB-borne malware (common in labs), shoulder surfing. Protections: strong passwords, 2FA, antivirus, software updates, safe browsing, backups, access control, avoid unknown USB drives. Reporting incidents to school IT/teacher.


## Worked Examples


### Example 3.1: Class List as Table

**Context**: Maintaining student info.

**Problem**: Show how fields and records are organized.

**Solution**:
```
Table 'Students' with fields: StudentID (PK), Name, Class, Phone. Each row is one student's record.
```

**Skills Tested**: Data organization, Primary key concept


### Example 3.2: Identifying Phishing

**Context**: SMS claims bank account will be blocked; link provided.

**Problem**: Decide if safe and why.

**Solution**:
```
Likely phishing: urgent language, unknown link. Verify via official channels; do not click; report.
```

**Skills Tested**: Cyber awareness, Decision making


### Example 3.3: Backing Up a School Project

**Context**: ICT club project on lab PC only.

**Problem**: Propose a simple backup plan.

**Solution**:
```
Copy to flash drive and cloud (if available); version by date; store offsite; reduces loss from power or malware.
```

**Skills Tested**: Backup strategy, Risk mitigation


## Practice Problems


### Basic Level


**3.1.B**: Define data and information.

> **Answer**: Data: raw facts; Information: processed, meaningful data.

> **Explanation**: Key distinction.


**3.2.B**: What is a record in a table?

> **Answer**: A row containing related fields about one item/person.

> **Explanation**: Table structure.


**3.3.B**: Name one network device.

> **Answer**: Router (others: switch, modem, access point).

> **Explanation**: Network component recall.


### Core Level


**3.4.C**: State two reasons backups are important.

> **Answer**: Protect against hardware failure, malware, accidental deletion, theft.

> **Explanation**: Risk coverage.


**3.5.C**: Give two examples of malware.

> **Answer**: Virus, ransomware (others: worm, trojan).

> **Explanation**: Threat types.


**3.6.C**: Differentiate LAN and WAN in one line each.

> **Answer**: LAN: local network (school/building). WAN: wide-area network connecting distant sites.

> **Explanation**: Scope difference.


### Challenge Level


**3.7.CH**: Explain why using unknown USB drives is risky in school labs.

> **Answer**: They may carry malware that auto-runs and infects PCs; can spread across lab quickly.

> **Explanation**: Vector awareness.


**3.8.CH**: A table has fields: ID, Name, Class, Email. Identify a good primary key.

> **Answer**: ID (unique identifier).

> **Explanation**: Primary key uniqueness.


**3.9.CH**: State two simple steps to secure online banking on a phone.

> **Answer**: Use strong PIN/biometrics; enable 2FA/OTP; avoid public Wi-Fi; update apps; log out after use.

> **Explanation**: Practical safeguards.


**3.10.CH**: Why does low bandwidth cause slow downloads?

> **Answer**: Bandwidth limits data per second; lower bandwidth transfers less data over time, increasing download duration.

> **Explanation**: Bandwidth-speed link.


## Glossary


**Primary Key**: Field that uniquely identifies a record in a table.

- *Example*: StudentID.


**LAN**: Local Area Network within a limited area.

- *Example*: School network.


**Phishing**: Attempt to trick users into giving sensitive data via fake messages.

- *Example*: Fake bank SMS.


**Malware**: Malicious software such as viruses or ransomware.

- *Example*: Locky ransomware.


**Backup**: Copy of data stored separately for recovery.

- *Example*: Weekly flash drive copy.


## Assessment


### Quick Checks (Understanding Check)

1. What is a field?

2. Name one DBMS.

3. Give one difference between LAN and WAN.

4. State one sign of phishing.

5. Why use antivirus software?


### End-of-Lesson Quiz


**1. Data becomes information when:**

- It is stored

- It is processed for meaning

- It is typed

- It is deleted

> **Correct Answer**: It is processed for meaning


**2. A router is used to:**

- Print documents

- Connect networks

- Store data

- Compile code

> **Correct Answer**: Connect networks


**3. Phishing often uses:**

- Legit URLs

- Unexpected links/messages

- Strong encryption

- Local storage only

> **Correct Answer**: Unexpected links/messages


**4. Best unique identifier for students:**

- Name

- Class

- StudentID

- Address

> **Correct Answer**: StudentID


**5. Two-factor authentication adds:**

- A second password

- Another verification factor

- More storage

- Extra RAM

> **Correct Answer**: Another verification factor


### WAEC Exam-Style Questions


**1. Describe three common cybersecurity threats faced by students using public cybercafes and propose one control for each.**

> **Answer Guide**: Phishing (verify links); keyloggers/malware (antivirus, avoid unknown PCs); shoulder surfing (cover PIN, privacy screens); insecure Wi-Fi (avoid sensitive logins).


**2. Explain how data should be organized for a school's library system using tables and primary keys, and outline a simple backup approach suitable for limited internet access.**

> **Answer Guide**: Tables: Books, Students, Loans; PKs: BookID, StudentID, LoanID; backups to external drive weekly; optional cloud when available.


## Summary


This lesson covered the fundamentals of Computer Science at SS1 level.

Key topics included:

- 3.1: Data vs Information and Data Organization

- 3.2: Databases and File Systems

- 3.3: Networks and Data Transmission Basics

- 3.4: Cybersecurity Essentials


## Visual Aids & Resources


- **Table Structure Diagram** (diagram): Fields/records highlighting primary key.


- **Simple Network Map** (diagram): LAN with router, switch, Wi-Fi AP.


- **Cybersecurity Dos and Don'ts** (poster): Quick tips for labs and mobile banking.


---


**Prepared for**: Computer Science SS1

**WAEC Tags**: data vs information, databases, tables and records, LAN, WAN...

**Learning Path**: Unit 1 → Data and Cybersecurity Fundamentals
