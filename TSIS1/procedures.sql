CREATE OR REPLACE PROCEDURE add_phone(p_contact_name VARCHAR, p_phone VARCHAR, p_type VARCHAR)
LANGUAGE plpgsql AS $$
DECLARE v_id INTEGER;
BEGIN
    SELECT id INTO v_id FROM contacts WHERE name = p_contact_name LIMIT 1;
    IF v_id IS NULL THEN RAISE EXCEPTION 'Contact "%" not found', p_contact_name; END IF;
    INSERT INTO phones (contact_id, phone, type) VALUES (v_id, p_phone, p_type);
END;
$$;
 
CREATE OR REPLACE PROCEDURE move_to_group(p_contact_name VARCHAR, p_group_name VARCHAR)
LANGUAGE plpgsql AS $$
DECLARE v_cid INTEGER; v_gid INTEGER;
BEGIN
    SELECT id INTO v_cid FROM contacts WHERE name = p_contact_name LIMIT 1;
    IF v_cid IS NULL THEN RAISE EXCEPTION 'Contact "%" not found', p_contact_name; END IF;
    SELECT id INTO v_gid FROM groups WHERE name = p_group_name LIMIT 1;
    IF v_gid IS NULL THEN INSERT INTO groups (name) VALUES (p_group_name) RETURNING id INTO v_gid; END IF;
    UPDATE contacts SET group_id = v_gid WHERE id = v_cid;
END;
$$;
 
CREATE OR REPLACE FUNCTION search_contacts(p_query TEXT)
RETURNS TABLE (id INTEGER, name VARCHAR, email VARCHAR, birthday DATE, grp VARCHAR, phones TEXT)
LANGUAGE plpgsql AS $$
BEGIN
    RETURN QUERY
    SELECT c.id, c.name, c.email, c.birthday, g.name,
           STRING_AGG(p.phone || ' (' || COALESCE(p.type, '?') || ')', ', ')
    FROM contacts c
    LEFT JOIN groups g ON g.id = c.group_id
    LEFT JOIN phones p ON p.contact_id = c.id
    WHERE c.name ILIKE '%' || p_query || '%'
       OR c.email ILIKE '%' || p_query || '%'
       OR p.phone ILIKE '%' || p_query || '%'
    GROUP BY c.id, c.name, c.email, c.birthday, g.name;
END;
$$;
 