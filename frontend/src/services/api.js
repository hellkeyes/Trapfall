// every page imports here
const BASE_URL = "http://127.0.0.1:8000";

export async function registerUser(userData){
    const response = await fetch(`${BASE_URL}/auth/register`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(userData),
    });

    return response;
}


export async function loginUser(userData){
    const response = await fetch(`${BASE_URL}/auth/login`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(userData),
    });

    return response;
}


export async function createRoom(token){
    const response = await fetch(`${BASE_URL}/rooms/create`,{
        method: 'POST',
        headers: {
            'Authorization': `Bearer ${token}`,
            'Content-Type': 'application/json',
        },
    });
    return response
}


export async function joinRoom(roomCode, token){
    const response = await fetch(`${BASE_URL}/rooms/${roomCode}/join`,{
        method: 'POST',
        headers: {
            'Authorization': `Bearer ${token}`,
            'Content-Type': 'application/json',
        },
    });
    return response
}

export async function getRoom(roomCode, token){

    const response = await fetch(`${BASE_URL}/rooms/${roomCode}`, {
        method: "GET",
        headers: {
            "Authorization": `Bearer ${token}`,
            "Content-Type": "application/json",
        },
    });

    return response;
}