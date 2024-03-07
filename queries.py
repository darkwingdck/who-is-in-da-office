QUERIES = {
    # users
    'add_user': '''
        INSERT INTO User (id, name, company_id)
        VALUES ("{id}", "{name}", "{company_id}");
        ''',

    'get_users': '''
        SELECT id, name FROM User
        WHERE presence = true and company_id = (
            SELECT company_id FROM User
            WHERE id = "{user_id}"
        );
        ''',

    'update_user_presence': '''
        UPDATE User SET presence = {presence}
        WHERE id = "{id}";
        ''',

    'update_user_lunch_id': '''
        UPDATE User SET lunch_id = {lunch_id}
        WHERE id = "{id}";
        ''',

    'get_user': '''
        SELECT * FROM User
        WHERE id = "{id}";
        ''',

    # lunch
    'get_lunches': '''
        SELECT id, name, votes_count FROM Lunch
        WHERE company_id = (
            SELECT company_id FROM User
            WHERE id = "{user_id}"
        )
        ORDER BY votes_count DESC;
        ''',

    'increase_lunch_votes_count': '''
        UPDATE Lunch SET votes_count = votes_count + 1
        WHERE id = {id};
        ''',

    'decrease_lunch_votes_count': '''
        UPDATE Lunch SET votes_count = votes_count - 1
        WHERE id = {id};
        ''',

    'add_lunch': '''
        INSERT INTO Lunch (name, company_id)
        VALUES ("{name}", "{company_id}");
        ''',

    # company
    'add_company': '''
        INSERT INTO Company (id, name)
        VALUES ("{id}", "{name}");
        ''',

    'get_company': '''
        SELECT id, name, employees_count FROM Company
        WHERE id = (
            SELECT company_id FROM User
            WHERE id = "{user_id}"
        );
        ''',

    'get_companies': '''
        SELECT id, name, employees_count FROM Company;
        ''',
}
