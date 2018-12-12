import {Injectable} from '@angular/core';
import {HttpClient} from '@angular/common/http';
import {environment} from '../../environments/environment';

@Injectable({
  providedIn: 'root'
})
export class PlayerService {

  constructor(private http: HttpClient) {
  }

  isPlaying() {
    return this.http.get(`${environment.apiUrl}/player/play_pause`);
  }

  play(username, state) {
    return this.http.put(`${environment.apiUrl}/player/play_pause/${username}/${state}`, null);
  }

  getNext() {
    return this.http.get(`${environment.apiUrl}/player/next`);
  }

  next(username) {
    return this.http.put(`${environment.apiUrl}/player/next/${username}`, null);
  }

  getPrev() {
    return this.http.get(`${environment.apiUrl}/player/previous`);
  }

  prev(username) {
    return this.http.put(`${environment.apiUrl}/player/previous/${username}`, null);
  }

  isShuffle() {
    return this.http.get(`${environment.apiUrl}/player/shuffle`);
  }

  shuffle(username) {
    return this.http.put(`${environment.apiUrl}/player/play_pause/${username}`, null);
  }

  isRepeat() {
    return this.http.get(`${environment.apiUrl}/player/repeat`);
  }

  repeat(username) {
    return this.http.put(`${environment.apiUrl}/player/play_pause/${username}`, null);
  }
}
