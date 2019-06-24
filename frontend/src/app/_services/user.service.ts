import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { environment } from '../../environments/environment';
import { User } from '../_models';
import { Buffer } from 'buffer';
import * as blake2b from 'blake2b';

@Injectable()
export class UserService {
    constructor(private http: HttpClient) {
    }

    async getUser() {
        try {
            return await this.http.get(`${environment.apiUrl}/users/me`).toPromise();
        } catch (err) {
            console.log(err);
        }
    }

    async register(user: User) {
        try {
            return await this.http.post(`${environment.apiUrl}/register`, user).toPromise();
        } catch (err) {
            console.log(err);
        }
    }
}

function hashPwd(user: User) {
    const input = Buffer.from(user.password);
    const proto = blake2b(64);
    proto.update(input);
    user.password = proto.digest('hex');
    return user;
}
