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

  isPlaying() {
    return this.http.get(`${environment.apiUrl}/player/play-pause`);
  }

  playPause(username) {
      return this.http.put(`${environment.apiUrl}/player/play-pause`, JSON.stringify({'username': username}));
  }

  getNext() {
    return this.http.get(`${environment.apiUrl}/player/next`);
  }

  next(username) {
    return this.http.put(`${environment.apiUrl}/player/next`, JSON.stringify({'username': username}));
  }

  getPrev() {
    return this.http.get(`${environment.apiUrl}/player/previous`);
  }

  prev(username) {
    return this.http.put(`${environment.apiUrl}/player/previous`,
      JSON.stringify({'username': username}));
  }

  isShuffle() {
    return this.http.get(`${environment.apiUrl}/player/shuffle`);
  }

  shuffle(username) {
    return this.http.put(`${environment.apiUrl}/player/shuffle`,
      JSON.stringify({'username': username}));
  }

  isLoop() {
    return this.http.get(`${environment.apiUrl}/player/loop`);
  }

  loop(username) {
    return this.http.put(`${environment.apiUrl}/player/loop`,
      JSON.stringify({'username': username}));
  }

  listSongs() {
    return this.http.get(`${environment.apiUrl}/list`);
  }

  updatedb() {
    return this.http.put(`${environment.apiUrl}/update`, JSON.stringify({}));
  }
}
