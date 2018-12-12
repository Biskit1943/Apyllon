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

  play() {
    return this.http.put(`${environment.apiUrl}/player/play_pause`, null);
  }

  getNext() {
    return this.http.get(`${environment.apiUrl}/player/next`);
  }

  next() {
    return this.http.put(`${environment.apiUrl}/player/next`, null);
  }

  getPrev() {
    return this.http.get(`${environment.apiUrl}/player/previous`);
  }

  prev() {
    return this.http.put(`${environment.apiUrl}/player/previous`, null);
  }

  isShuffle() {
    return this.http.get(`${environment.apiUrl}/player/shuffle`);
  }

  shuffle() {
    return this.http.put(`${environment.apiUrl}/player/play_pause`, null);
  }

  isRepeat() {
    return this.http.get(`${environment.apiUrl}/player/repeat`);
  }

  repeat() {
    return this.http.put(`${environment.apiUrl}/player/play_pause`, null);
  }
}
