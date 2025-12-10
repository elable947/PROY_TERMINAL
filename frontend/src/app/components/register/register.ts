import { Component, inject, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormBuilder, FormGroup, Validators, ReactiveFormsModule } from '@angular/forms';
import { Router, RouterModule } from '@angular/router';
import { AuthService } from '../../services/auth.service';
import { DataService } from '../../services/data.service';

@Component({
  selector: 'app-register',
  standalone: true,
  imports: [CommonModule, ReactiveFormsModule, RouterModule],
  templateUrl: './register.html',
  styleUrl: './register.css'
})
export class Register implements OnInit {
  private fb = inject(FormBuilder);
  private authService = inject(AuthService);
  private router = inject(Router);

  registerForm: FormGroup = this.fb.group({
    idTipoUsuario: ['1', Validators.required], // Always 1 (Pasajero)
    nombre_usuario: ['', Validators.required],
    dni: ['', [Validators.minLength(8)]],
    apPaterno: ['', Validators.required],
    apMaterno: ['', Validators.required],
    correo: ['', [Validators.required, Validators.email]],
    password: ['', [Validators.required, Validators.minLength(6)]],
    telefono: ['', Validators.required],
    edad: ['', [Validators.required, Validators.min(18)]]
  });

  errorMessage: string = '';
  isLoading: boolean = false;
  showSuccessModal: boolean = false;

  constructor() { }

  closeModal() {
    this.showSuccessModal = false;
    this.router.navigate(['/login']);
  }

  ngOnInit() {
    // No need to load companies anymore
  }

  onSubmit() {
    if (this.registerForm.invalid) {
      this.registerForm.markAllAsTouched();
      return;
    }

    this.isLoading = true;
    this.errorMessage = '';

    const formData = this.registerForm.value;
    formData.idTipoUsuario = 1; // Enforce Pasajero
    formData.idPais = 135; // Default Peru (135)

    // Ensure conversion
    if (!formData.dni) delete formData.dni;

    this.authService.register(formData).subscribe({
      next: (res) => {
        this.isLoading = false;
        this.showSuccessModal = true; // Show Custom Modal
      },
      error: (err) => {
        this.isLoading = false;
        console.error('Register error', err);
        this.errorMessage = err.error?.error || 'Error al registrar usuario';
      }
    });
  }
}
