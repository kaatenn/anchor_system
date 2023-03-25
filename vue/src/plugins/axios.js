import axios from 'axios'
import Cookies from "js-cookie";

const httpGet = axios.create({
        baseURL: '/api/',
        timeout: 3000
    }
)

const httpPost = axios.create({
        baseURL: '/api/',
        timeout: 3000
    }
)

const httpDelete = axios.create({
        baseURL: '/api/',
        timeout: 3000
    }
)

httpPost.interceptors.request.use(config => {
    config.headers['Content-Type'] = 'application/x-www-form-urlencoded; charset=UTF-8'
    config.headers['X-Requested-With'] = 'XMLHttpRequest'
    config.headers['X-CSRFToken'] = Cookies.get('csrftoken')
    return config
})

httpPost.interceptors.response.use(
    response => {
        return response
    },
    error => {
        return Promise.reject(error)
    }
)

httpDelete.interceptors.request.use(config => {
    config.headers['X-CSRFToken'] = Cookies.get('csrftoken')
    return config
})

httpPost.interceptors.response.use(
    response => {
        return response
    },
    error => {
        return Promise.reject(error)
    }
)

export {httpGet, httpPost, httpDelete}