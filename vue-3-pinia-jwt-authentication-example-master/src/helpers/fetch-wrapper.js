import { useAuthStore } from '@/stores'
import { router } from './router'

export const fetchWrapper = {
    get: request('GET'),
    post: request('POST'),
    put: request('PUT'),
    delete: request('DELETE'),
    patch: request('PATCH')
}

export const sendFile = {
    get: requestFile('GET'),
    post: requestFile('POST'),
    put: requestFile('PUT'),
    delete: requestFile('DELETE'),
    patch: requestFile('PATCH')
}

function request(method) {
  //change it to async for better code readability
    return (url, body) => {
        const requestOptions = {
            method,
            headers: authHeader(url)
        }
        if (body) {
            requestOptions.headers['Content-Type'] = 'application/json'
            requestOptions.body = JSON.stringify(body)
        }
        console.log(requestOptions,url,body)
        return fetch(url, requestOptions).then(handleResponse)
    }
}

// request for files

function requestFile(method) {
    return (url, body) => {
        const requestOptions = {
            method,
            headers: authHeader(url)
        }
        if (body) {
            requestOptions.body = body
        }
        return fetch(url, requestOptions).then(handleResponse)
    }
}

// helper functions

function authHeader(url) {
    // return auth header with jwt if user is logged in and request is to the api url
    const { user } = useAuthStore()
    const isLoggedIn = !!user?.tokens
    const isApiUrl = url.startsWith(import.meta.env.VITE_API_URL)
    if (isLoggedIn && isApiUrl) {
        return { Authorization: `Bearer ${user.tokens.access}` }
    } else {
        return {}
    }
}

function handleResponse(response) {
    return response.text().then(text => {
        const data = text && JSON.parse(text)
        if (!response.ok) {
            const { user } = useAuthStore()
            if ([401, 403].includes(response.status) && user) {
                // auto logout if 401 Unauthorized or 403 Forbidden response returned from api
                console.log(response.status)
                router.push("/")
            }
            
            const error = (data && data.message) || response.statusText
            return Promise.reject(error)
        }
        
        return data
    })
}    
