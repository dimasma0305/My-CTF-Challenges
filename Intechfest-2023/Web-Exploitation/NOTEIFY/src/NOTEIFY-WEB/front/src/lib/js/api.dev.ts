
const apiEndpoint = "http://localhost:8080"

// Login function
export async function login(username: string, password: string) {
  const response = await fetch(`${apiEndpoint}/api/login`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify({ username, password })
  });
  return response
}

// Register function
export async function register(username: string, password: string) {
  const response = await fetch(`${apiEndpoint}/api/register`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify({ username, password })
  });
  return response  
}


export async function getnote(noteid: string) {
  const response = await fetch(`${apiEndpoint}/api/getnote/${noteid}`, {
    method: "GET",
    headers: {
      "Authorization": `Bearer ${localStorage.bearerToken}`
    }
  })
  return response
}

export async function addnote(title: string, content: string) {
  const response = await fetch(`${apiEndpoint}/api/addnote`, {
    method: "POST",
    headers: {
      "Authorization": `Bearer ${localStorage.bearerToken}`,
      "Content-Type": "application/json"
    },
    body: JSON.stringify({ title, content })
  })
  return response
}

export async function getnotes() {
  const response = await fetch(`${apiEndpoint}/api/getnotes`, {
    method: "GET",
    headers: {
      "Authorization": `Bearer ${localStorage.bearerToken}`,
      "Content-Type": "application/json"
    },
  })
  return response
}