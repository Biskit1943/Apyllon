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

    async play() {
        try {
            return await this.http.put(`${environment.apiUrl}/player/play`, {}).toPromise();
        } catch (err) {
            console.log(err);
        }
    }

    async playSong(song_path) {
        try {
            const song = {'song_path': song_path, 'type': 3};
            return await this.http.put(`${environment.apiUrl}/player/playsong`, JSON.stringify(song)).toPromise();
        } catch (err) {
            throw err;
        }
    }

    async pause() {
        try {
            return await this.http.put(`${environment.apiUrl}/player/pause`, {}).toPromise();
        } catch (err) {
            console.log(err);
        }
    }

    async stop() {
        try {
            return await this.http.put(`${environment.apiUrl}/player/stop`, {}).toPromise();
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

    shuffle() {
        try {
            return this.http.put(`${environment.apiUrl}/player/shuffle`, {}).toPromise();
        } catch (err) {
            throw (err);
        }
    }

    isLoop() {
        return this.http.get(`${environment.apiUrl}/player/state`).pipe(map(response => {
            if (response && response.hasOwnProperty('loop')) {
                return response['loop'] === 'true';
            }
        })).toPromise();
    }

    loop() {
        try {
            return this.http.put(`${environment.apiUrl}/player/loop`, {}).toPromise();
        } catch (err) {
            throw (err);
        }
    }

    async listSongs() {
        try {
            const response = await this.http.get(`${environment.apiUrl}/player/playlist`).toPromise();
            return response && response.hasOwnProperty('songs') ? response['songs'] : [];
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
