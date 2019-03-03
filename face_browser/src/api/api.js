import axios from 'axios'

// const baseUrl = "https://api.zmrj.site/api/v1.0/"
// const baseUrl = "http://face.njunova.com/api/v1.0/"
const baseUrl = "http://127.0.0.1:5000/api/v1.0/"
const loginUrl = baseUrl + 'Authentication'
const PhotoUrl = baseUrl + 'Photo'
const adminLoginUrl = baseUrl + 'adminAuth'
const checkItemUrl = baseUrl + 'checkItem'
const configUrl = baseUrl + 'appConfig'
const userListUrl = baseUrl + 'userTable'
const checkListUrl = baseUrl + 'checkList'
const adminListUrl = baseUrl + 'adminTable'
// // http request 拦截器
// axios.interceptors.request.use(
//     config => {
//         if (localStorage.getItem('token')) {  // 判断是否存在token，如果存在的话，则每个http header都加上token
//             config.headers.Authorization = `Token ${localStorage.getItem('token')}`;
//         }
//         if (localStorage.getItem('adminToken')) {  // 判断是否存在token，如果存在的话，则每个http header都加上token
//             config.headers.Authorization = `adminToken ${localStorage.getItem('adminToken')}`;
//         }
//         return config;
//     },
//     err => {
//         return Promise.reject(err);
//     });


export default {
    // 用户登陆
    getToken(username, password, resolve, reject) {
        axios.get(
            loginUrl, {
                auth: { username: username, password: password }
            }
        ).then(resolve).catch(reject)
    },
    // 用户获取照片
    getPhoto(resolve, reject) {
        axios.get(PhotoUrl, {
                headers: {
                    Authorization: `Token ${localStorage.getItem('token')}`
                }
            }).then(resolve).catch(reject)
    },
    // 注册（未开通）
    register(username, password, phone, resolve, reject) {
        axios.post(
            loginUrl, {username, password, phone}
        ).then(resolve).catch(reject)    
    },
    // 用户上传照片
    uploadPhoto(img, resolve, reject) {
        let form = new FormData()
        form.append('img',img, img.name)
        axios.put(PhotoUrl,form, {
            headers: {
                Authorization: `Token ${localStorage.getItem('token')}`
            }
        })
        .then(resolve).catch(reject)
    },
    // 管理员登陆
    getAdminToken(username, password, resolve, reject) {
        axios.get(
            adminLoginUrl, {
                auth: { username: username, password: password }
            }
        ).then(resolve).catch(reject)
    },
    // 审核员获取审核数据
    getCheckItem(resolve, reject) {
        axios.get(checkItemUrl, {
            headers: {
                Authorization: `adminToken ${localStorage.getItem('adminToken')}`
            }
        }).then(resolve).catch(reject)
    },
    // 审核员审核
    postCheckItem(id,pass,mark,resolve,reject) {
        axios.post(checkItemUrl,{id, pass, mark},{
            headers: {
                Authorization: `adminToken ${localStorage.getItem('adminToken')}`
            }
        }).then(resolve).catch(reject)
    },
    // 获取系统配置
    getConfig(resolve,reject) {
        axios.get(configUrl, {
            headers: {
                Authorization: `adminToken ${localStorage.getItem('adminToken')}`
            }
        }).then(resolve).catch(reject)
    },
    // 修改配置
    saveConfig(host, photoLength, photoWidth, photoFormat, dir, confidence, resolve) {
        axios.put(configUrl, {host, photoLength, photoWidth, photoFormat: '.' + photoFormat  , dir, confidence}, {
            headers: {
                Authorization: `adminToken ${localStorage.getItem('adminToken')}`
            }
        }).then(resolve)
    },

    // 获取用户列表
    getUserList(resolve) {
        axios.get(userListUrl, {
            headers: {
                Authorization: `adminToken ${localStorage.getItem('adminToken')}`
            }
        }).then(resolve)
    },
    getCheckList(resolve) {
        axios.get(checkListUrl, {
            headers: {
                Authorization: `adminToken ${localStorage.getItem('adminToken')}`
            }
        }).then(resolve)
    },
    // 管理员修改
    editCheckItem(username,status, remark, resolve) {
        axios.put(checkItemUrl, {username, status, remark}, {
            headers: {
                Authorization: `adminToken ${localStorage.getItem('adminToken')}`
            }
        }).then(resolve)
    },
    addSingleUser(username, password, photo, resolve) {
        let form = new FormData()
        form.append('photo',photo, photo.name)
        form.append('username',username)
        form.append('password',password)
        form.append('type',1)
        axios.post(userListUrl, form, {
            headers: {
                Authorization: `adminToken ${localStorage.getItem('adminToken')}`
            }
        }).then(resolve)
    },
    deleteUser(username, resolve) {
        axios.delete(userListUrl, {
            data: {
                username: username  
            },
            headers: {
                Authorization: `adminToken ${localStorage.getItem('adminToken')}`
            }
        }).then(resolve)
    },
    addUsers(data, zipFile, resolve) {
        let form = new FormData()
        let tempBlob = new Blob([zipFile], {type: "application/zip"})
        form.append('zipFile', tempBlob)
        form.append('data',JSON.stringify(data))
        form.append('type',2)
        axios.post(userListUrl, form, {
            headers: {
                Authorization: `adminToken ${localStorage.getItem('adminToken')}`
            }
        }).then(resolve)
    },
    getadminList(resolve) {
        axios.get(adminListUrl, {
            headers: {
                Authorization: `adminToken ${localStorage.getItem('adminToken')}`
            }
        }).then(resolve)
    },
    addAdmin(adminname, password, permission, resolve) {
        axios.post(adminListUrl, {adminname, password, permission}, {
            headers: {
                Authorization: `adminToken ${localStorage.getItem('adminToken')}`
            }
        }).then(resolve)
    },
    deleteAdmin(adminname, resolve) {
        axios.delete(adminListUrl, {data: {adminname: adminname}, headers: {
            Authorization: `adminToken ${localStorage.getItem('adminToken')}`
        }}).then(resolve)
    }

}