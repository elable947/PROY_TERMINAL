import { Component, signal } from '@angular/core';
import { RouterOutlet } from '@angular/router';
import { Navbar } from './components/navbar/navbar';
import { Footer } from './components/footer/footer';
import { ToastComponent } from './components/toast/toast';

@Component({
  selector: 'app-root',
  imports: [RouterOutlet, Navbar, Footer, ToastComponent],
  templateUrl: './app.component.html',
  styleUrl: './app.css'
})
export class App {
  protected readonly title = signal('frontend');
}
