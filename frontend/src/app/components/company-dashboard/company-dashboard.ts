import { Component, inject, OnInit, ChangeDetectorRef } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormBuilder, FormGroup, Validators, ReactiveFormsModule, FormsModule } from '@angular/forms';
import { AuthService } from '../../services/auth.service';
import { CompanyService } from '../../services/company.service';
import { ToastService } from '../../services/toast.service';
import Swal from 'sweetalert2';

@Component({
  selector: 'app-company-dashboard',
  standalone: true,
  imports: [CommonModule, ReactiveFormsModule, FormsModule],
  templateUrl: './company-dashboard.html',
  styleUrl: './company-dashboard.css'
})
export class CompanyDashboard implements OnInit {
  activeTab: string = 'general';

  // Data lists
  // Data lists
  drivers: any[] = [];
  vehicles: any[] = [];
  filteredVehicles: any[] = []; // New
  filterType: string = '';      // New

  trips: any[] = [];
  promos: any[] = [];
  routes: any[] = [];
  vehicleTypes: any[] = [];
  socials: any[] = []; // New

  // Locations
  departments: any[] = [];
  provinces: any[] = [];
  provDestinations: any[] = [];

  currentUser: any = null;
  idEmpresa: number = 0;
  companyDetails: any = null;
  selectedFile: File | null = null;

  // Forms
  driverForm: FormGroup;
  vehicleForm: FormGroup;
  tripForm: FormGroup;
  promoForm: FormGroup;
  routeForm: FormGroup;
  newDestForm: FormGroup;
  socialForm: FormGroup; // New

  // Edit/Modal States
  isEditingDriver = false;
  currentDriverId: number | null = null;
  foundUser: any = null;

  isEditingVehicle = false;
  currentVehicleId: number | null = null;

  isCreatingDest = false;
  defaultOriginId: number | null = null;

  showDriverModal = false; // Controls modal visibility

  // Services
  private fb = inject(FormBuilder);
  private authService = inject(AuthService);
  private companyService = inject(CompanyService);
  private toastService = inject(ToastService);
  private cdr = inject(ChangeDetectorRef);
  constructor() {
    // Driver Form
    this.driverForm = this.fb.group({
      dni: ['', [Validators.required, Validators.minLength(8)]],
      licencia: ['', Validators.required],
      estado: [true] // New field for active/inactive
    });

    // Vehicle Form
    this.vehicleForm = this.fb.group({
      placa: ['', Validators.required],
      modelo: [''],
      capacidadAsientos: [40, Validators.required],
      idTipoVehiculo: ['', Validators.required]
    });

    // Trip Form
    this.tripForm = this.fb.group({
      idVehiculo: ['', Validators.required],
      idConductorEmpresa: ['', Validators.required],
      idRuta: ['', Validators.required],
      fechaSalida: ['', Validators.required],
      precio: [0, [Validators.required, Validators.min(1)]]
    });

    // Promo Form
    this.promoForm = this.fb.group({
      nombrePromocion: ['', Validators.required],
      descripcionPromocion: [''],
      valorDescuento: [0, Validators.required],
      fechaInicio: ['', Validators.required],
      fechaFin: ['', Validators.required]
    });

    // Route Form
    this.routeForm = this.fb.group({
      deptId: ['', Validators.required],
      provId: ['', Validators.required],
      idDestino: ['', Validators.required],
      duracionAprox: ['', Validators.required],
      distanciakm: ['', Validators.required],
      idOrigen: [{ value: '', disabled: true }] // Display only
    });

    // New Destination Form
    this.newDestForm = this.fb.group({
      nombreDestino: ['', Validators.required]
    });

    // Social Form
    this.socialForm = this.fb.group({
      red: ['Facebook', Validators.required],
      url: ['', [Validators.required]]
    });
  }

  ngOnInit() {
    this.authService.currentUser$.subscribe(user => {
      this.currentUser = user;
      if (user && user.idEmpresaTransporte) {
        this.idEmpresa = user.idEmpresaTransporte;
        this.loadAll();
      }
    });
    this.loadDepartments();
    this.findDefaultOrigin();
  }

  setTab(tab: string) {
    this.activeTab = tab;
  }

  loadAll() {
    this.loadCompanyDetails();
    this.loadDrivers();
    this.loadVehicles();
    this.loadTrips();
    this.loadPromos();
    this.loadRoutes();
    this.loadVehicleTypes();
    this.loadSocials(); // New
  }

  // --- LOADERS ---
  loadCompanyDetails() {
    this.companyService.getCompanyDetails(this.idEmpresa).subscribe({
      next: (data) => this.companyDetails = data,
      error: (err) => console.error('Error loading company details', err)
    });
  }

  loadDrivers() {
    this.companyService.getDrivers(this.idEmpresa).subscribe(data => this.drivers = data);
  }
  loadVehicles() {
    this.companyService.getVehicles(this.idEmpresa).subscribe(data => {
      this.vehicles = data;
      this.applyVehicleFilter(); // Initial filter
    });
  }

  applyVehicleFilter() {
    if (!this.filterType) {
      this.filteredVehicles = this.vehicles;
    } else {
      this.filteredVehicles = this.vehicles.filter(v => v.idTipoVehiculo.toString() === this.filterType);
    }
  }

  loadTrips() {
    this.companyService.getTrips(this.idEmpresa).subscribe(data => this.trips = data);
  }
  loadPromos() {
    this.companyService.getPromos().subscribe(data => this.promos = data);
  }
  loadRoutes() {
    this.companyService.getRoutes().subscribe(data => this.routes = data);
  }
  loadVehicleTypes() {
    this.companyService.getVehicleTypes().subscribe(data => this.vehicleTypes = data);
  }
  loadDepartments() {
    this.companyService.getDepartments().subscribe({
      next: (data) => {
        this.departments = data;
      },
      error: (err: any) => {
        console.error(err);
        this.toastService.show('Error loading departments: ' + (err.message || err.statusText), 'error');
      }
    });
  }

  // --- BANNER ACTIONS ---
  onBannerSelected(event: any) {
    this.selectedFile = (event.target as HTMLInputElement).files?.[0] || null;
  }

  uploadBanner() {
    if (!this.selectedFile) return;

    const formData = new FormData();
    formData.append('banner', this.selectedFile);
    formData.append('idEmpresaTransporte', this.idEmpresa.toString());

    this.companyService.uploadBanner(formData).subscribe({
      next: (res: any) => {
        this.toastService.show('Banner actualizado', 'success');
        if (this.companyDetails) {
          // Update local URL with timestamp to force refresh
          this.companyDetails.bannerUrl = res.url + '?t=' + new Date().getTime();
        }
        this.selectedFile = null;
      },
      error: (err: any) => this.toastService.show('Error subiendo banner', 'error')
    });
  }

  // --- DRIVER ACTIONS ---
  searchUser() {
    const dni = this.driverForm.get('dni')?.value;
    if (!dni) return;

    this.companyService.findUserByDni(dni).subscribe({
      next: (user) => {
        this.foundUser = user;
        this.toastService.show('Usuario encontrado', 'info');
      },
      error: () => {
        this.foundUser = null;
        this.toastService.show('Usuario no encontrado', 'error');
      }
    });
  }

  assignDriver() {
    if (this.isEditingDriver && this.currentDriverId) {
      const payload = {
        idEmpresaTransporte: this.idEmpresa,
        licencia: this.driverForm.get('licencia')?.value,
        estado: this.driverForm.get('estado')?.value ? 1 : 0
      };
      this.companyService.updateDriver(this.currentDriverId, payload).subscribe(() => {
        this.toastService.show('Conductor actualizado exitosamente', 'success');
        this.loadDrivers();
        this.cancelEditDriver();
      });
      return;
    }

    if (!this.foundUser || this.driverForm.invalid) return;

    const payload = {
      idUsuario: this.foundUser.idUsuario,
      idEmpresaTransporte: this.idEmpresa,
      licencia: this.driverForm.get('licencia')?.value
    };

    this.companyService.assignDriver(payload).subscribe({
      next: () => {
        this.toastService.show('Conductor asignado exitosamente', 'success');
        this.loadDrivers();
        this.driverForm.reset();
        this.foundUser = null;
      },
      error: (err: any) => this.toastService.show('Error al asignar conductor', 'error')
    });
  }

  editDriver(d: any) {
    this.isEditingDriver = true;
    this.currentDriverId = d.idConductorEmpresa;
    this.foundUser = d;
    this.driverForm.patchValue({
      dni: d.dni,
      licencia: d.licencia,
      estado: d.estadoConductorEmpresa // Patch status
    });
    this.showDriverModal = true;
  }

  deleteDriver(d: any) {
    Swal.fire({
      title: '¿Eliminar conductor?',
      text: "El conductor será desvinculado.",
      icon: 'warning',
      showCancelButton: true,
      confirmButtonColor: '#3085d6',
      cancelButtonColor: '#d33',
      confirmButtonText: 'Sí, eliminar',
      cancelButtonText: 'Cancelar'
    }).then((result) => {
      if (result.isConfirmed) {
        this.companyService.deleteDriver(d.idConductorEmpresa, this.idEmpresa).subscribe({
          next: () => {
            Swal.fire('Eliminado', 'Conductor eliminado.', 'success');
            // Force local removal immediately for visual feedback
            this.drivers = this.drivers.filter(dr => dr.idConductorEmpresa !== d.idConductorEmpresa);
            this.cdr.detectChanges();
            // Then reload from server
            this.loadDrivers();
          },
          error: (err) => {
            console.error(err);
            const msg = err.error?.error || 'No se pudo eliminar.';
            Swal.fire('Error', msg, 'error');
          }
        });
      }
    });
  }

  openAddDriverModal() {
    this.isEditingDriver = false;
    this.currentDriverId = null;
    this.foundUser = null;
    this.driverForm.reset({ estado: true });
    this.showDriverModal = true;
  }

  cancelEditDriver() {
    this.isEditingDriver = false;
    this.currentDriverId = null;
    this.foundUser = null;
    this.driverForm.reset();
    this.showDriverModal = false;
  }

  // --- VEHICLE ACTIONS ---
  createVehicle() {
    if (this.vehicleForm.invalid) return;
    const payload = { ...this.vehicleForm.value, idEmpresaTransporte: this.idEmpresa };

    if (this.isEditingVehicle && this.currentVehicleId) {
      this.companyService.updateVehicle(this.currentVehicleId, payload).subscribe(() => {
        this.toastService.show('Vehículo actualizado', 'success');
        this.cancelEditVehicle();
        this.loadVehicles();
      });
    } else {
      this.companyService.registerVehicle(payload).subscribe(() => {
        this.toastService.show('Vehículo registrado', 'success');
        this.loadVehicles();
        this.vehicleForm.reset({ capacidadAsientos: 40, idTipoVehiculo: '' });
      });
    }
  }

  editVehicle(v: any) {
    this.isEditingVehicle = true;
    this.currentVehicleId = v.idVehiculo;
    this.vehicleForm.patchValue({
      placa: v.placa,
      capacidadAsientos: v.capacidadAsientos,
      idTipoVehiculo: v.idTipoVehiculo
    });
  }

  deleteVehicle(v: any) {
    Swal.fire({
      title: '¿Eliminar vehículo?',
      text: "Esta acción no se puede deshacer.",
      icon: 'warning',
      showCancelButton: true,
      confirmButtonColor: '#3085d6',
      cancelButtonColor: '#d33',
      confirmButtonText: 'Sí, eliminar',
      cancelButtonText: 'Cancelar'
    }).then((result) => {
      if (result.isConfirmed) {
        this.companyService.deleteVehicle(v.idVehiculo, this.idEmpresa).subscribe({
          next: () => {
            Swal.fire('Eliminado', 'El vehículo ha sido eliminado.', 'success');
            this.loadVehicles();
          },
          error: (err) => Swal.fire('Error', 'No se pudo eliminar el vehículo.', 'error')
        });
      }
    });
  }

  cancelEditVehicle() {
    this.isEditingVehicle = false;
    this.currentVehicleId = null;
    this.vehicleForm.reset({ capacidadAsientos: 40, idTipoVehiculo: '' });
  }

  // --- TRIP ACTIONS ---
  createTrip() {
    if (this.tripForm.invalid) return;
    const payload = { ...this.tripForm.value, idEmpresaTransporte: this.idEmpresa };
    this.companyService.createTrip(payload).subscribe({
      next: () => {
        this.toastService.show('Viaje programado exitosamente', 'success');
        this.loadTrips();
        this.tripForm.reset();
      },
      error: (err: any) => {
        console.error(err);
        this.toastService.show(err.error?.error || 'Error al programar viaje', 'error');
      }
    });
  }

  // --- PROMO ACTIONS ---
  createPromo() {
    if (this.promoForm.invalid) return;
    this.companyService.createPromo(this.promoForm.value).subscribe(() => {
      this.toastService.show('Promoción publicada', 'success');
      this.loadPromos();
      this.promoForm.reset();
    });
  }

  // --- ROUTE ACTIONS ---
  onDeptChange() {
    const deptId = this.routeForm.get('deptId')?.value;
    this.provinces = [];
    this.provDestinations = [];
    this.routeForm.patchValue({ provId: '', idDestino: '' });
    if (deptId) {
      this.companyService.getProvinces(deptId).subscribe(data => this.provinces = data);
    }
  }

  onProvChange() {
    const provId = this.routeForm.get('provId')?.value;
    this.provDestinations = [];
    this.routeForm.patchValue({ idDestino: '' });
    if (provId) {
      this.companyService.getDestinationsByProv(provId).subscribe(data => this.provDestinations = data);
    }
  }

  findDefaultOrigin() {
    this.companyService.getTerminals().subscribe({
      next: (terms) => {
        // Find Chachapoyas Terminal
        const chacha = terms.find(t => t.nombreTerminal && t.nombreTerminal.toLowerCase().includes('chachapoyas'));
        if (chacha) {
          this.defaultOriginId = chacha.idTerminal;
        } else {
          console.warn('Terminal Chachapoyas no encontrado', terms);
          this.defaultOriginId = 1; // Fallback to Terminal 1
        }
      },
      error: (err: any) => {
        console.error('Error fetching terminals', err);
        this.defaultOriginId = 1; // Fallback hardcoded
      }
    });
  }

  openNewDestModal() {
    if (!this.routeForm.get('provId')?.value) {
      this.toastService.show('Seleccione una provincia primero', 'info');
      return;
    }
    this.isCreatingDest = true;
  }

  closeNewDestModal() {
    this.isCreatingDest = false;
    this.newDestForm.reset();
  }

  saveNewDest() {
    if (this.newDestForm.invalid) return;
    const provId = this.routeForm.get('provId')?.value;
    const payload = {
      idProvincia: provId,
      nombreDestino: this.newDestForm.get('nombreDestino')?.value
    };

    this.companyService.createDestination(payload).subscribe({
      next: (res: any) => {
        this.toastService.show('Destino creado', 'success');
        this.closeNewDestModal();
        this.companyService.getDestinationsByProv(provId).subscribe(data => {
          this.provDestinations = data;
          this.routeForm.patchValue({ idDestino: res.idDestino });
        });
      },
      error: (err: any) => this.toastService.show('Error al crear destino', 'error')
    });
  }

  createRoute() {
    if (this.routeForm.invalid) {
      this.toastService.show('Complete el formulario', 'info');
      return;
    }
    if (!this.defaultOriginId) {
      this.toastService.show('No se ha definido el origen (Terminal no detectado).', 'error');
      // Try to find it again? 
      // Force 1 if desperate?
      this.defaultOriginId = 1;
      // return; // Let it try with 1
    }

    const payload = {
      idOrigen: this.defaultOriginId,
      idDestino: this.routeForm.get('idDestino')?.value,
      duracionAprox: this.routeForm.get('duracionAprox')?.value,
      distanciakm: this.routeForm.get('distanciakm')?.value
    };

    this.companyService.createRoute(payload).subscribe({
      next: () => {
        this.toastService.show('Ruta creada exitosamente', 'success');
        this.loadRoutes();
        this.routeForm.reset();
        // Reset origin?
        this.findDefaultOrigin();
      },
      error: (err: any) => this.toastService.show(err.error?.message || 'Error al crear ruta', 'error')
    });
  }

  // --- SOCIAL ACTION ---
  loadSocials() {
    this.companyService.getSocials(this.idEmpresa).subscribe(data => this.socials = data);
  }

  addSocial() {
    if (this.socialForm.invalid) return;
    const payload = {
      idEmpresaTransporte: this.idEmpresa,
      red: this.socialForm.get('red')?.value,
      url: this.socialForm.get('url')?.value
    };
    this.companyService.addSocial(payload).subscribe({
      next: () => {
        this.toastService.show('Red social agregada', 'success');
        this.loadSocials();
        this.socialForm.reset({ red: 'Facebook' });
      },
      error: (err: any) => this.toastService.show('Error al agregar red social', 'error')
    });
  }

  deleteSocial(id: number) {
    if (confirm('¿Eliminar red social?')) {
      this.companyService.deleteSocial(id, this.idEmpresa).subscribe({
        next: () => {
          this.toastService.show('Red social eliminada', 'success');
          this.loadSocials();
        },
        error: (err: any) => this.toastService.show('Error al eliminar red social', 'error')
      });
    }
  }
}
