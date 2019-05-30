import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { environment } from '../../environments/environment';
import { map } from "rxjs/operators";

@Injectable({
    providedIn: 'root'
})
export class PlayerService {
    constructor(private http: HttpClient) {
    }

    async isPlaying() {
        try {
            const res = await this.getState();
            if (res && res.hasOwnProperty('state')) {
                return res['state'] === 'play';
            }
            return false;
        } catch (err) {
            console.log(err);
        }
    }

    async currentSong() {
        try {
            const state = await this.getState();
            if (state && state.hasOwnProperty('current')) {
                return state['current'];
            }
        } catch (err) {
            console.log(err);
        }
    }

    async playPause() {
        try {
            if (await this.isPlaying()) {
                return await this.http.put(`${environment.apiUrl}/player/pause`, {}).toPromise();
            } else {
                return await this.http.put(`${environment.apiUrl}/player/play`, {}).toPromise();
            }
        } catch (err) {
            console.log(err);
        }
    }

    async getNext() {
        try {
            const res = await this.getState();
            if (res && res.hasOwnProperty('next')) {
                return res['next'];
            }
        } catch (err) {
            console.log(err);
        }
    }

    async next() {
        try {
            return await this.http.put(`${environment.apiUrl}/player/next`, {}).toPromise();
        } catch (err) {
            console.log(err);
        }
    }

    async getPrev() {
        try {
            const res = await this.getState();
            if (res && res.hasOwnProperty('previous')) {
                return res['previous'];
            }
        } catch (err) {
            console.log(err);
        }
    }

    async prev() {
        try {
            return await this.http.put(`${environment.apiUrl}/player/previous`, {}).toPromise();
        } catch (err) {
            console.log(err);
        }
    }

    isShuffle() {
        return this.http.get(`${environment.apiUrl}/player/state`).pipe(map(response => {
            if (response && response.hasOwnProperty('shuffle')) {
                return response['shuffle'] === 'true';
            }
        })).toPromise();
    }

    shuffle(username) {
        return this.http.put(`${environment.apiUrl}/player/shuffle`,
            JSON.stringify({'username': username}));
    }

    isLoop() {
        return this.http.get(`${environment.apiUrl}/player/state`).pipe(map(response => {
            if (response && response.hasOwnProperty('loop')) {
                return response['loop'] === 'true';
            }
        })).toPromise();
    }

    loop(username) {
        return this.http.put(`${environment.apiUrl}/player/loop`,
            JSON.stringify({'username': username}));
    }

    async listSongs() {
        try {
            const response = await this.http.get(`${environment.apiUrl}/player/playlist`).toPromise();
            return response && response.hasOwnProperty('songs') ? response['songs'].map(song => song.meta.title) : [];
        } catch (err) {
            console.log(err);
        }
    }

    async getState() {
        try {
            return await this.http.get(`${environment.apiUrl}/player/state`).toPromise();
        } catch (err) {
            console.log(err);
        }
    }

    async addSongToPlaylist(path, type) {
        return this.http.put(`${environment.apiUrl}/player/playlist/add`, JSON.stringify({
            'song_path': path,
            'type': type
        }));
    }
}
