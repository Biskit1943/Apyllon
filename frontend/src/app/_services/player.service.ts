import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { environment } from '../../environments/environment';

@Injectable({
  providedIn: 'root'
})
export class PlayerService {

  constructor(private http: HttpClient) {
  }

  isPlaying() {
    return this.http.get(`${environment.apiUrl}/player/play-pause`);
  }

  play(username, state) {
    return this.http.put(`${environment.apiUrl}/player/play-pause/`,
      JSON.stringify({'username': username, 'state': state}));
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
    return this.http.put(`${environment.apiUrl}/player/previous/${username}`,
      JSON.stringify({'username': username}));
  }

  isShuffle() {
    return this.http.get(`${environment.apiUrl}/player/shuffle`);
  }

  shuffle(username) {
    return this.http.put(`${environment.apiUrl}/player/shuffle/${username}`,
      JSON.stringify({'username': username}));
  }

  isRepeat() {
    return this.http.get(`${environment.apiUrl}/player/loop`);
  }

  repeat(username) {
    return this.http.put(`${environment.apiUrl}/player/repeat/${username}`,
      JSON.stringify({'username': username}));
  }
}
