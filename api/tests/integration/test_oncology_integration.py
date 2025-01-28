from faker import Faker


fake = Faker()


def create_user() -> dict:
    name = fake.name().upper()
    while len(name) < 10:
        name = fake.name().upper()
    return {
        "code": fake.name().upper().replace(" ", ""),
        "name": name,
        "email": fake.email(),
        "hashed_password": fake.password(),
    }


def create_patient() -> dict:
    name = fake.name().upper()
    while len(name) < 10:
        name = fake.name().upper()
    return {
        "dni": fake.random_int(min=10000000, max=99999999),
        "name": name,
        "birth_date": fake.date_of_birth(minimum_age=1, maximum_age=90).isoformat(),
        "sex_id": fake.random_int(min=1, max=2),
        "weight": fake.random_number(digits=2, fix_len=False),
        "height": fake.random_number(digits=3, fix_len=False) / 10,
    }


def create_vital_signs(patient_id) -> dict:
    return {
        "patient_id": patient_id,
        "temperature": fake.pyfloat(min_value=36.0, max_value=40.0, right_digits=1),
        "systolic_pressure": fake.random_int(min=80, max=120),
        "diastolic_pressure": fake.random_int(min=80, max=120),
        "pulse_rate": fake.random_int(min=60, max=100),
        "respiration_rate": fake.random_int(min=12, max=20),
    }


def test_add_patient(test_client, initialize_user_and_session):
    payload = create_patient()
    response = test_client.post("/oncology/patient/", json=payload)

    assert response.status_code == 200
    data = response.json()
    assert data["dni"] == payload["dni"]
    assert data["name"] == payload["name"].upper()
    assert data["birth_date"] == payload["birth_date"]


def test_update_patient(test_client, initialize_user_and_session, db_session_client):
    payload = create_patient()
    response = test_client.post("/oncology/patient/", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["dni"] == payload["dni"]

    patient_id = data["id"]
    assert patient_id == 1
    upload_payload = {"id": patient_id, "name": fake.name()}

    response = test_client.put("/oncology/patient/", json=upload_payload)

    updated_data = response.json()
    assert data["name"] != updated_data["name"]


def test_create_user_then_patient_and_then_get_patients_user_empty(
    test_client, initialize_user_and_session
):
    patient_payload = create_patient()
    response = test_client.post("/oncology/patient/", json=patient_payload)
    response.json()["id"]

    user_payload = create_user()

    response = test_client.post("/management/users/", json=user_payload)
    user_id = response.json()["id"]

    response = test_client.get("/oncology/user/patient/?user_id=" + str(user_id))
    user_patients = response.json()

    assert user_patients["code"] == user_patients["code"]


def test_assign_patient_to_user(test_client, initialize_user_and_session):
    patient_payload = create_patient()
    patient_response = test_client.post("/oncology/patient/", json=patient_payload)
    patient_id = patient_response.json()["id"]

    user_id = fake.random_int(min=1, max=1000)

    assign_payload = {
        "user_id": user_id,
        "patient_id": patient_id,
    }
    assign_response = test_client.post("/oncology/user/patient/", json=assign_payload)

    assert assign_response.status_code == 200
    data = assign_response.json()
    assert data["user_id"] == assign_payload["user_id"]
    assert data["patient_id"] == assign_payload["patient_id"]


def test_register_vital_signs(test_client, initialize_user_and_session):
    patient_payload = create_patient()
    patient_response = test_client.post("/oncology/patient/", json=patient_payload)
    patient_id = patient_response.json()["id"]

    vital_signs_payload = create_vital_signs(patient_id)
    response = test_client.post(
        "/oncology/patient/vitalsigns/", json=vital_signs_payload
    )

    assert response.status_code == 200
    data = response.json()
    assert data["patient_id"] == vital_signs_payload["patient_id"]
    assert data["temperature"] == str(vital_signs_payload["temperature"])


def test_register_action(test_client, initialize_user_and_session):
    patient_payload = create_patient()
    patient_response = test_client.post("/oncology/patient/", json=patient_payload)
    patient_id = patient_response.json()["id"]

    action_payload = {
        "patient_id": patient_id,
        "action_id": fake.random_int(min=1, max=5),
        "comment": fake.text(max_nb_chars=50),
    }
    response = test_client.post("/oncology/patient/action/", json=action_payload)

    assert response.status_code == 200
    data = response.json()
    assert data["patient_id"] == action_payload["patient_id"]
    assert data["action_id"] == action_payload["action_id"]


def test_register_two_actions_and_retrieve_patient_registry(
    test_client, initialize_user_and_session
):
    patient_payload = create_patient()
    patient_response = test_client.post("/oncology/patient/", json=patient_payload)
    patient_id = patient_response.json()["id"]

    action_id_1 = fake.random_int(min=1, max=5)

    action_payload = {
        "patient_id": patient_id,
        "action_id": action_id_1,
        "comment": fake.text(max_nb_chars=50),
    }
    response = test_client.post("/oncology/patient/action/", json=action_payload)

    action_payload_2 = {
        "patient_id": patient_id,
        "action_id": fake.random_int(min=1, max=5),
        "comment": fake.text(max_nb_chars=50),
    }
    response = test_client.post("/oncology/patient/action/", json=action_payload_2)

    response = test_client.get(
        "/oncology/patient/action/?action_id="
        + str(action_id_1)
        + "&patient_id="
        + str(patient_id)
    )
    data = response.json()

    assert response.status_code == 200
    assert len(data) == 1
