Changelog
=========

19.0.1.4.0 (2026-05-20)
-----------------------
* Security: cascading groups (Patient → Intern → Doctor → Manager →
  Administrator) and record rules for visits.
* Patient: added ``user_id`` for record-rule linkage.
* Tests: unit tests for category uniqueness, ``is_intern`` compute,
  mentor constraint, doctor-history display name, disease recursion,
  patient age compute.
* Ukrainian translation (``i18n/uk.po``) including disease classifier.
* Added ``README.rst``, ``changelog.rst`` and module description page.

19.0.1.3.0
----------
* Block 5: PDF report for Doctor (visit history with colored statuses,
  patients table), kanban dropdown menu with color picker and
  intern list.

19.0.1.2.0
----------
* Block 4: list/form/calendar/pivot/graph/searchpanel for visits;
  patient quick visit; doctor kanban; hierarchical searchpanel for
  diseases; visit & disease report wizards.

19.0.1.1.0
----------
* Block 3: abstract medic.info model, doctor category & history,
  visit lifecycle, disease hierarchy, mass-reassign and visit report
  wizards.

19.0.1.0.0
----------
* Block 2: initial models — doctor, patient, disease, visit.
