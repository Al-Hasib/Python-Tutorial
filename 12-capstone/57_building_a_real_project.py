"""
Building a Real Project: A Capstone Contact Book Application
==============================================================

This is the capstone project for the whole curriculum. It ties together
fundamentals (variables, strings, numbers), control flow (if/else, loops),
data structures (lists, dicts), functions (default/keyword arguments),
error handling (custom exceptions, try/except), file/JSON handling, and
object-oriented programming (classes, encapsulation, special methods)
into one small but complete command-line style application: a Contact Book.

The program is written to run completely non-interactively. Instead of
blocking on real input() calls, it simulates a realistic sequence of user
actions (add, list, update, delete, save, load) directly in code and
prints the result of every step, the same way a human tester would drive
the program interactively. It also includes a handful of assert-based
self-checks that behave like lightweight unit tests, proving the core
behavior is correct every time the file is run.

Any file this script writes to disk for persistence demonstration purposes
is removed again before the script exits, so running it leaves no trace
in the repository.

This file covers:
- Custom exceptions for invalid input (error handling)
- A Contact class demonstrating classes & encapsulation (OOP)
- A ContactBook class using dicts/lists as the in-memory data store
- Functions with default and keyword arguments
- JSON file persistence: saving to and loading from disk
- assert-based self-checks (mini unit tests)
- A scripted, non-interactive demo that exercises the whole workflow
"""

import json
import os

# ---------------------------------------------------------------------------
# 1. Custom exceptions (Demonstrates: error handling / custom exceptions)
# ---------------------------------------------------------------------------


class ContactBookError(Exception):
    """Base class for all errors raised by this application."""


class InvalidContactError(ContactBookError):
    """Raised when contact data fails validation (e.g. bad name/phone)."""


class ContactNotFoundError(ContactBookError):
    """Raised when an operation refers to a contact that does not exist."""


# ---------------------------------------------------------------------------
# 2. The Contact class (Demonstrates: classes & encapsulation)
# ---------------------------------------------------------------------------


class Contact:
    """A single contact record.

    Uses a "private" attribute (prefixed with underscore) plus a property
    to demonstrate encapsulation: callers cannot set an empty/blank name
    directly, they must go through validation.
    """

    def __init__(self, name, phone="", email=""):
        self._name = ""  # set via the property setter below, for validation
        self.name = name
        self.phone = phone
        self.email = email

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        if not isinstance(value, str) or not value.strip():
            raise InvalidContactError("Contact name must be a non-empty string.")
        self._name = value.strip()

    def to_dict(self):
        """Convert this contact into a plain dict (for JSON serialization)."""
        return {"name": self.name, "phone": self.phone, "email": self.email}

    @classmethod
    def from_dict(cls, data):
        """Build a Contact back from a plain dict (loaded from JSON)."""
        return cls(name=data["name"], phone=data.get("phone", ""), email=data.get("email", ""))

    def __repr__(self):
        return "Contact(name={!r}, phone={!r}, email={!r})".format(self.name, self.phone, self.email)

    def __str__(self):
        parts = [self.name]
        if self.phone:
            parts.append("phone: " + self.phone)
        if self.email:
            parts.append("email: " + self.email)
        return " | ".join(parts)


# ---------------------------------------------------------------------------
# 3. The ContactBook class (Demonstrates: list/dict data structures,
#    functions with default & keyword arguments)
# ---------------------------------------------------------------------------


class ContactBook:
    """Stores contacts in a dict keyed by lower-cased name for fast lookup,
    while also being able to produce them as an ordered list."""

    def __init__(self):
        self._contacts = {}  # dict[str, Contact] -- the core data structure

    def add_contact(self, name, phone="", email="", *, overwrite=False):
        """Add a new contact. `phone` and `email` are optional keyword-friendly
        defaults; `overwrite` is a keyword-only flag controlling whether an
        existing contact with the same name may be replaced."""
        key = name.strip().lower()
        if key in self._contacts and not overwrite:
            raise InvalidContactError(
                "A contact named '{}' already exists (pass overwrite=True to replace).".format(name)
            )
        contact = Contact(name=name, phone=phone, email=email)
        self._contacts[key] = contact
        return contact

    def update_contact(self, name, *, phone=None, email=None):
        """Update fields of an existing contact. Only fields explicitly
        passed (not None) are changed -- a demonstration of default args
        used as "leave unchanged" sentinels."""
        key = name.strip().lower()
        if key not in self._contacts:
            raise ContactNotFoundError("No contact named '{}' was found.".format(name))
        contact = self._contacts[key]
        if phone is not None:
            contact.phone = phone
        if email is not None:
            contact.email = email
        return contact

    def delete_contact(self, name):
        key = name.strip().lower()
        if key not in self._contacts:
            raise ContactNotFoundError("No contact named '{}' was found.".format(name))
        return self._contacts.pop(key)

    def find_contact(self, name):
        return self._contacts.get(name.strip().lower())

    def list_contacts(self, sort_by="name"):
        """Return all contacts as a list, sorted by the given field."""
        contacts = list(self._contacts.values())
        if sort_by == "name":
            contacts.sort(key=lambda c: c.name.lower())
        elif sort_by == "phone":
            contacts.sort(key=lambda c: c.phone)
        return contacts

    def __len__(self):
        return len(self._contacts)

    # -----------------------------------------------------------------------
    # 4. JSON file persistence (Demonstrates: file & JSON handling)
    # -----------------------------------------------------------------------

    def save_to_file(self, filepath):
        """Save all contacts to a JSON file."""
        data = [contact.to_dict() for contact in self.list_contacts()]
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)
        return filepath

    def load_from_file(self, filepath):
        """Load contacts from a JSON file, replacing current in-memory data."""
        with open(filepath, "r", encoding="utf-8") as f:
            data = json.load(f)
        self._contacts = {}
        for item in data:
            contact = Contact.from_dict(item)
            self._contacts[contact.name.lower()] = contact
        return len(self._contacts)


# ---------------------------------------------------------------------------
# 5. Self-checks (Demonstrates: assert-based mini unit tests)
# ---------------------------------------------------------------------------


def run_self_checks():
    """A handful of assert-based checks that verify core behavior.
    These act like lightweight unit tests, run every time this file executes.
    """
    print("Running self-checks...")

    # -- Adding and validating contacts --
    book = ContactBook()
    book.add_contact("Alice Smith", phone="555-0101", email="alice@example.com")
    assert len(book) == 1
    assert book.find_contact("alice smith") is not None
    assert book.find_contact("ALICE SMITH").phone == "555-0101"

    # -- Duplicate names are rejected unless overwrite=True --
    try:
        book.add_contact("Alice Smith", phone="000-0000")
        assert False, "expected InvalidContactError for duplicate contact"
    except InvalidContactError:
        pass  # expected

    # -- Invalid (blank) names are rejected --
    try:
        Contact(name="   ")
        assert False, "expected InvalidContactError for blank name"
    except InvalidContactError:
        pass  # expected

    # -- Updating only touches the fields provided --
    book.update_contact("Alice Smith", email="alice.new@example.com")
    updated = book.find_contact("Alice Smith")
    assert updated.phone == "555-0101"  # unchanged
    assert updated.email == "alice.new@example.com"  # changed

    # -- Deleting a contact removes it, and re-deleting raises --
    book.add_contact("Bob Jones", phone="555-0202")
    assert len(book) == 2
    book.delete_contact("Bob Jones")
    assert len(book) == 1
    try:
        book.delete_contact("Bob Jones")
        assert False, "expected ContactNotFoundError for missing contact"
    except ContactNotFoundError:
        pass  # expected

    # -- Save/load round-trip preserves data --
    check_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "_selfcheck_contacts.json")
    try:
        book.save_to_file(check_path)
        reloaded = ContactBook()
        reloaded.load_from_file(check_path)
        assert len(reloaded) == len(book)
        assert reloaded.find_contact("Alice Smith").email == "alice.new@example.com"
    finally:
        if os.path.exists(check_path):
            os.remove(check_path)

    print("All self-checks passed.\n")


# ---------------------------------------------------------------------------
# 6. Non-interactive demo (Demonstrates: the full workflow, end to end)
# ---------------------------------------------------------------------------


def run_demo():
    """Simulate a realistic sequence of user actions against the contact
    book, printing the outcome of every step. No real input() is used --
    the "user actions" are just a scripted list of operations."""

    data_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "contacts_demo.json")
    book = ContactBook()

    print("=== Contact Book Demo ===\n")

    # Step 1: add some contacts
    print("Step 1: Adding contacts...")
    for name, phone, email in [
        ("Grace Hopper", "555-1001", "grace@example.com"),
        ("Ada Lovelace", "555-1002", "ada@example.com"),
        ("Alan Turing", "555-1003", "alan@example.com"),
    ]:
        contact = book.add_contact(name, phone=phone, email=email)
        print("  Added:", contact)
    print()

    # Step 2: list all contacts, sorted by name
    print("Step 2: Listing all contacts (sorted by name)...")
    for contact in book.list_contacts(sort_by="name"):
        print("  -", contact)
    print()

    # Step 3: update a contact
    print("Step 3: Updating Alan Turing's phone number...")
    book.update_contact("Alan Turing", phone="555-9999")
    print("  Updated record:", book.find_contact("Alan Turing"))
    print()

    # Step 4: try an invalid operation and handle the error gracefully
    print("Step 4: Attempting to add a duplicate contact (should fail cleanly)...")
    try:
        book.add_contact("Ada Lovelace", phone="000-0000")
    except InvalidContactError as exc:
        print("  Caught expected error:", exc)
    print()

    # Step 5: delete a contact
    print("Step 5: Deleting Grace Hopper...")
    removed = book.delete_contact("Grace Hopper")
    print("  Removed:", removed)
    print("  Remaining contact count:", len(book))
    print()

    # Step 6: save to a JSON file next to this script
    print("Step 6: Saving contact book to disk as JSON...")
    saved_path = book.save_to_file(data_file)
    print("  Saved to:", saved_path)
    with open(saved_path, "r", encoding="utf-8") as f:
        print("  Raw JSON contents:")
        print("  " + f.read().replace("\n", "\n  "))
    print()

    # Step 7: load into a brand new ContactBook instance to prove persistence works
    print("Step 7: Loading contact book from disk into a fresh instance...")
    fresh_book = ContactBook()
    count = fresh_book.load_from_file(data_file)
    print("  Loaded {} contact(s):".format(count))
    for contact in fresh_book.list_contacts():
        print("  -", contact)
    print()

    # Step 8: clean up the demo file so the repository stays clean
    print("Step 8: Cleaning up the demo data file...")
    if os.path.exists(data_file):
        os.remove(data_file)
        print("  Removed:", data_file)
    print()

    print("=== Demo complete ===")


# ---------------------------------------------------------------------------
# 7. Entry point
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    run_self_checks()
    run_demo()


# Key takeaways:
# - Real projects combine many small concepts (OOP, exceptions, data
#   structures, functions, and file I/O) into one cohesive program.
# - Encapsulation (e.g. a validated `name` property) keeps invalid data
#   out of your objects instead of trusting every caller to be careful.
# - Custom exception classes make error handling specific and readable,
#   letting callers catch exactly the failure they expect.
# - JSON is a simple, human-readable way to persist Python data structures
#   to disk and load them back into equivalent objects.
# - assert-based self-checks, run automatically, catch regressions early
#   and document expected behavior directly in the code.
