===================
Hospital Management
===================

Module for hospital automation: doctors, patients, diseases, visits,
reporting and wizards.

Features
========

* Doctors with qualifications, mentor/intern relations.
* Patients with personal-doctor history and medical attributes
  (blood type, gender, age, insurance, phone).
* Visits with state machine (Planned / Completed / Cancelled).
* Diseases as a hierarchical classifier with searchpanel.
* Wizards: mass reassign personal doctor, visits report, monthly
  diseases report.
* PDF report for a doctor with visit history and patient list.
* Cascading security groups: Patient → Intern → Doctor → Manager →
  Administrator with record rules.
* Ukrainian translation.

Installation
============

#. Copy the ``hr_hospital`` folder into your Odoo addons directory.
#. Update the apps list and install the module from **Apps**.

Usage
=====

After installation a new top-level menu **Hospital** appears with
sub-menus for Patients, Doctors, Visits, and Configuration
(Diseases, Doctor Categories, Doctor history).

Bug Tracker
===========

Issues are reported via GitHub: https://github.com/AnnaKhoro/odoo_hospital_module/issues

Credits
=======

Authors
-------

* Anna Khoroshylova

License
=======

LGPL-3
