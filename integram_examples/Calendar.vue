<template>
  <div>
    <div class="md-layout">
      <md-card>
        <md-card-header class="md-card-header-icon md-card-header-green">
          <div class="card-icon">
            <md-icon>home</md-icon>
          </div>
          <h4 class="title">Appointments & Slots</h4>
        </md-card-header>
        <nav-tabs-card>
          <template slot="content">
            <span class="md-nav-tabs-title">
            </span>
            <md-tabs  class="md-success" md-alignment="centered">
              <md-tab id="tab-calendar" class="md-success" md-label="Map" md-icon="map">
                <div style="font-size: 35px; text-align: center">
                  <md-radio v-if="what_to_show === 'requests'" v-model="what_to_show" name="requests" id="requests" value="requests"><span style="color: green; font-weight: bold">Show Requests only</span></md-radio>
                  <md-radio v-else-if="what_to_show !== 'requests' || what_to_show !== 'all'" v-model="what_to_show" name="requests" id="requests" value="requests">Show Requests only</md-radio>
                  
                  <md-radio v-if="what_to_show === 'slots'" v-model="what_to_show" name="slots" id="slots" value="slots"><span style="color: green; font-weight: bold">Show Slots only</span></md-radio>
                  <md-radio v-else-if="what_to_show !== 'slots' || what_to_show !== 'all'" v-model="what_to_show" name="slots" id="slots" value="slots">Show Slots only</md-radio>

                  <md-radio v-if="what_to_show === 'all'" v-model="what_to_show" name="all" id="all" value="all"><span style="color: green; font-weight: bold">Show Both</span></md-radio>
                  <md-radio v-else-if="what_to_show !== 'all'" v-model="what_to_show" name="all" id="all" value="all">Show Both</md-radio>
                </div>
              <md-card style="border-style: solid;">
                <md-card-content>
                  <div class="md-layout">
                      <div class="md-layout-item md-size-30" style="text-align: left">
                        <md-button class="md-danger" style="border-style: solid;" :disabled="disable_backward_button" v-on:click="backAmonth()"><md-icon>arrow_back_ios</md-icon></md-button>
                      </div>
                      <div class="md-layout-item md-size-40" style="text-align: center">
                        <h5 style="padding: 0px; margin: 0px;">Selected Range</h5>
                        <h3 style="padding: 0px; margin: 0px;"><b>{{this.current_start_date + '   to   ' + this.current_end_date}}</b></h3>
                      </div>
                      <div class="md-layout-item md-size-30" style="text-align: right">
                        <md-button class="md-danger" style="border-style: solid;" v-on:click="forwardAmonth()"><md-icon>arrow_forward_ios</md-icon></md-button>
                      </div>
                  </div>
                </md-card-content>
              </md-card>
                <md-card class="md-layout-item md-size-100" style="border-style: solid;">
                  <md-card-header>
                    <div class="md-layout">
                      <div class="md-layout-item md-size-30">
                        <md-card-content>
                          <label for="supported_products" style="font-size: 20px; font-weight: bold">Supported Products</label>
                            <br>
                            <select
                              class="select-style label-style"
                              md-size="auto"
                              v-model="selected_supported_product"
                              name="selected_supported_product"
                              id="selected_supported_product"
                              md-selected="-"
                              >
                              <option value="-">
                                -
                              </option>
                              <option v-for="{id, name} in this.product_types" :key="id" :value="id">
                                {{ name }}
                              </option>
                            </select>

                          <md-autocomplete
                            v-if="show_normal_booking"
                            autocomplete="off"
                            class="search"
                            md-input-name="current_selected_expert_search_input"
                            v-model="selectedExpert"
                            :md-options="selected_experts"
                            :md-open-on-focus="true"
                            required
                            disabled
                            @md-changed="getExperts">
                            <label v-if="selectedExpert">Expert</label>
                            <label v-else>Search Expert.. (temporarily disabled)</label>
                          </md-autocomplete>
                          <md-autocomplete
                            v-if="show_normal_booking"
                            autocomplete="off"
                            class="search"
                            md-input-name="current_selected_venue_search_input"
                            v-model="selectedVenue"
                            :md-options="venues"
                            :md-open-on-focus="true"
                            required
                            @md-changed="getVenues">
                            <label v-if="selectedVenue">Venue</label>
                            <label v-else>Search Venue..</label>
                          </md-autocomplete>
                        </md-card-content>
                      </div>
                      <div class="md-layout-item md-size-10">
                      </div>
                      <div class="md-layout-item md-size-30">
                        <md-card-content>
                          <md-checkbox v-if="show_normal_booking" autocomplete="off" v-model="venue_parking" name="venue_parking" id="venue_parking"><b><span class="label-style">Free Parking</span></b></md-checkbox>
                          <br>
                          <md-checkbox v-if="show_normal_booking" autocomplete="off" v-model="venue_disable_access" name="venue_disable_access" id="venue_disable_access"><b><span class="label-style">Disable Access</span></b></md-checkbox>
                          <br>
                          <md-checkbox v-if="show_normal_booking" autocomplete="off" v-model="venue_lift_access" name="venue_lift_access" id="venue_lift_access"><b><span class="label-style">Lift Access</span></b></md-checkbox>
                          <br>
                          <md-checkbox v-if="show_normal_booking" autocomplete="off" v-model="venue_child_friendly" name="venue_child_friendly" id="venue_child_friendly"><b><span class="label-style">Children Friendly</span></b></md-checkbox>
                        </md-card-content>
                      </div>
                      <!-- <div class="md-layout-item md-size-20">
                        <div class="md-layout">
                          <div class="md-layout-item md-size-100">
                            <md-datepicker v-model="selectedDate"/>
                          </div>
                          <div class="md-layout-item md-size-50">
                            <md-switch v-model="showAppointments" class="md-primary" id="show_appointments_switch">
                              <label v-if="showAppointments">Appointments</label>
                              <label v-else>Slots</label>
                            </md-switch>
                          </div>
                          <div class="md-layout-item md-size-50">
                              <md-button class="md-icon-button md-just-icon md-success md-round" @click.native="printReport">
                                <md-icon>print</md-icon>
                                <md-tooltip><b>Print</b> current schedule</md-tooltip>
                              </md-button>
                          </div>
                        </div>
                      </div> -->
                      <div class="md-layout-item md-size-25">
                        <h3 style="font-weight: bold">Select Attachments for Expert</h3>
                        <br>
                        <md-field>
                          <label style="font-size: 20px">Current Case Attachments<br></label>
                            <md-select
                              v-model="selected_attachments"
                              name="selected_attachments"
                              id="selected_attachments"
                              multiple>
                              <md-option   v-for="{id, type} in this.currentCase.attachments" :key="id" :value="id">
                              {{ type }}
                              </md-option>
                            </md-select>
                        </md-field>
                      </div>
                    </div>
                  </md-card-header>
                </md-card>
                <md-card>
                  <md-card-content v-if="show_normal_booking">
                    <md-field>
                      <label class="label-style" style="text-align: left; font-weight: bold">Internal slots retrieved:</label>
                      <md-input disabled v-model="internal_slots_counter"></md-input>
                    </md-field>
                    <br>
                    <md-field>
                      <label class="label-style" style="text-align: left; font-weight: bold">Easyslot slots retrieved:</label>
                      <md-input disabled v-model="easyslot_slots_counter"></md-input>
                    </md-field>
                    <div class="md-layout-item md-small-size-100" style="text-align: center">
                      <h2 v-if="currentCase.claimant.postcode" v-bind:style="{ color: 'green' }" style="padding: 0px; margin: 0px;">{{"Claimant's Postcode: " + currentCase.claimant.postcode}}</h2>
                      <h2 v-else v-bind:style="{ color: 'red' }" style="padding: 0px; margin: 0px;">{{"Claimant's Postcode: " + currentCase.claimant.postcode}}</h2>
                      <h3>Slide to choose radius</h3>
                      <div class="range-slider" v-for="slider in sliders" :key="slider.id">
                        <input class="range-slider__range" type="range" min="0" max="40" step="0.5" v-model="sla_radius">
                        <span class="range-slider__value"><h4>Current sla radius is set to: <b>{{sla_radius}}</b></h4></span>
                      </div>
                      <div style="text-align: center;">
                        <md-button class="md-primary" v-on:click="retrieveData()"><md-icon>room</md-icon>Retrieve data</md-button>
                      </div>
                      <br>
                    </div>
                    <div style="border-style: solid;" id="venueLocationsMap" class="map"></div>
                  </md-card-content>
                  <md-card-content v-else-if="!show_normal_booking && show_third_party_booking">
                    <div class="md-layout-item md-small-size-100" style="text-align: center; display: none">
                      <h2 v-if="currentCase.claimant.postcode" v-bind:style="{ color: 'green' }" style="padding: 0px; margin: 0px;">{{"Claimant's Postcode: " + currentCase.claimant.postcode}}</h2>
                      <h2 v-else v-bind:style="{ color: 'red' }" style="padding: 0px; margin: 0px;">{{"Claimant's Postcode: " + currentCase.claimant.postcode}}</h2>
                      <h3>Slide to choose radius</h3>
                      <div class="range-slider" v-for="slider in sliders" :key="slider.id">
                        <input class="range-slider__range" type="range" min="0" max="40" step="0.5" v-model="sla_radius">
                        <span class="range-slider__value"><h4>Current sla radius is set to: <b>{{sla_radius}}</b></h4></span>
                      </div>
                      <div style="border-style: solid;" id="venueLocationsMap" class="map"></div>
                    </div>
                    
                    <h1 style="text-align: center">Third party booking form</h1>

                    <label style="font-size: 20px; font-weight: bold;">Third party companies</label>
                    <br>
                    <select
                      style="font-size: 20px;"
                      md-size="auto"
                      v-model="adhocAppointment.selected_third_party"
                      name="selected_third_party"
                      id="selected_third_party"
                      md-selected="-"
                      >
                      <option value="-">
                        -
                      </option>
                      <option   v-for="{id, name} in this.third_party_companies" :key="id" :value="id">
                        {{ name }}
                      </option>
                    </select>
                    &nbsp;
                    <md-button class="md-success md-round" style="vertical-align:middle;" v-if="adhocAppointment.selected_third_party !== '-'" v-on:click="requestSlotThirdParty(adhocAppointment.selected_third_party)">Request Appointment</md-button>
                    <br>
                    <br>
                    <br>
                    <span style="font-size: 20px; font-weight: bold;">Venue</span>
                    <span>
                      <md-field>
                        <label>Name of the Venue</label>
                        <md-input v-model="adhocAppointment.venue"></md-input>
                        <span class="md-helper-text">Be careful, mistyping will not be corrected automatically!</span>
                      </md-field>
                    </span>
                    <br>
                    <br>
                    <br>
                    <span style= "display: block;">
                      <span style="position: initial !important; display: block; font-size: 20px; font-weight: bold;">Appointment Datetime</span>
                      <date-picker
                        width="300px"
                        v-model="adhocAppointment.datetime"
                        data-vv-name="adhocAppointment.datetime"
                        lang="en" 
                        type="datetime" 
                        format="[on] DD-MM-YYYY [at] HH:mm"
                        >
                      </date-picker>
                    </span>
                    <br>
                    <br>
                    <br>
                    <span style="font-size: 20px;font-weight: bold;">Appointment Notes</span>
                    <md-field>
                      <label>Notes</label>
                      <md-textarea v-model="adhocAppointment.notes"></md-textarea>
                    </md-field>
                    <br>
                    <br>
                    <br>
                    <md-button style="text-align: center" class="md-round md-success" v-if="adhocAppointment.venue && adhocAppointment.selected_third_party !== '-' && adhocAppointment.datetime" v-on:click="bookAdhocAppointment">Book Adhoc Appointment</md-button>
                  </md-card-content>
                  <md-card-content v-else style="display: none">
                    <div class="md-layout-item md-small-size-100" style="text-align: center">
                      <h2 v-if="currentCase.claimant.postcode" v-bind:style="{ color: 'green' }" style="padding: 0px; margin: 0px;">{{"Claimant's Postcode: " + currentCase.claimant.postcode}}</h2>
                      <h2 v-else v-bind:style="{ color: 'red' }" style="padding: 0px; margin: 0px;">{{"Claimant's Postcode: " + currentCase.claimant.postcode}}</h2>
                      <h3>Slide to choose radius</h3>
                      <div class="range-slider" v-for="slider in sliders" :key="slider.id">
                        <input class="range-slider__range" type="range" min="0" max="40" step="0.5" v-model="sla_radius">
                        <span class="range-slider__value"><h4>Current sla radius is set to: <b>{{sla_radius}}</b></h4></span>
                      </div>
                    </div>
                    <div style="border-style: solid;" id="venueLocationsMap" class="map"></div>
                  </md-card-content>
                </md-card>
              </md-tab>
              <!-- <md-tab id="tab-reserved-slots" class="md-success" md-label="Reserved Slots" md-icon="">
                <md-card>
                    <md-card-content>
                      <reserved-slots></reserved-slots>
                    </md-card-content>
                </md-card>
              </md-tab> -->
              <md-tab id="tab-map" class="md-success" md-label="" md-icon="">
                 <div class="md-layout-item md-small-size-100">
                  <md-card>
                    <md-card-content>
                      <div id="fullCalendar"></div>
                    </md-card-content>
                  </md-card>
                </div>
              </md-tab>
              <md-tab v-if="false" class="md-success" md-label="Expert Slot Request" md-icon="email">
                 <div class="md-layout-item md-small-size-100">
                  <md-card>
                    <md-card-content>
                      <appointment-request-multi-select-filter v-bind:current-case="currentCase"/>
                    </md-card-content>
                  </md-card>
                </div>
              </md-tab>
            </md-tabs>
          </template>
        </nav-tabs-card>
      </md-card>
    </div>
  </div>
</template>
<script>
import Vue from "vue"
import { mapActions } from 'vuex'
import { mapGetters } from 'vuex'
import moment from 'moment'

import Swal from "sweetalert2";
import $ from "jquery";
import "fullcalendar";
import { NavTabsCard } from "vue-material-dashboard-pro/src/components";
import { API_KEY } from "./GOOGLE_API_KEY";
import GoogleMapsLoader from "google-maps";
import AppointmentsList from "./AppointmentsList.vue";
import SlotSeriesGenerator from "./SlotSeriesGenerator.vue"
import AppointmentRequestMultiSelectFilter from "./AppointmentRequestMultiSelectFilter.vue";
import DatePicker from 'vue2-datepicker';
// import ReservedSlots from "./ReservedSlots.vue";


var jsPDF = require('jspdf')
require('jspdf-autotable')

GoogleMapsLoader.KEY = API_KEY;


var today = new Date();
var y = today.getFullYear();
var m = today.getMonth();
var d = today.getDate();

function claimantAppointmentNotificationPDF(item, return_content, adhoc=false){
  console.log(item.venue)
  console.log(item.appointment_type)
  const current_case_object = JSON.parse(sessionStorage.getItem('current_case_object'))
  var doc = new jsPDF('p', 'pt')
  let logoData = "data:image/jpg;base64,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"
  doc.setFontSize(12)
  doc.setFont('times','normal')
  doc.addImage(logoData, 'JPEG', -30, 15)

  var our_ref=current_case_object.claimant.last_name.substring(0,3) + current_case_object.id

  doc.text(40, 100, doc.splitTextToSize('Our Ref: ' + our_ref, 520), {align: "left"})
  doc.text(40, 120, doc.splitTextToSize('Solicitor Ref: ' + current_case_object.instructing_party.instruction_party_reference, 520), {align: "left"})
  
  
  var claimant_address = []
  claimant_address.push(current_case_object.claimant.title + ' ' + current_case_object.claimant.first_name + ' ' + current_case_object.claimant.last_name)
  if (current_case_object.claimant.address1){
    claimant_address.push(current_case_object.claimant.address1)
  }
  if (current_case_object.claimant.address2){
    claimant_address.push(current_case_object.claimant.address2)
  }
  if (current_case_object.claimant.address3){
    claimant_address.push(current_case_object.claimant.address3)
  }
  if (current_case_object.claimant.postcode){
    claimant_address.push(current_case_object.claimant.postcode)
  }
  doc.setFontSize(9)
  doc.setTextColor(150)
  doc.text(550, 40, ['Integra Medical Reporting Ltd',
                      'Building 3',
                      'Chiswick Park',
                      '566 Chiswick High Road', 
                      'Chiswick', 
                      'London', 
                      'W4 5YA',
                      'Tel: 0845 862 1909',
                      'Email: appointments@integramedical.co.uk',
                      'Website: https://www.integramedical.co.uk'
                      ], {align: "right"})

  doc.setTextColor(0, 0, 0)
  doc.setFont('times','bold')
  doc.setFontSize(12)
  doc.text(40, 180, claimant_address, {align: "left"})

  doc.setDrawColor(0)
  doc.setFillColor(255, 255, 255)
  doc.roundedRect(280, 170, 270, 120, 3, 3, 'FD')
  doc.setFont('times','bold')
  doc.text(283, 190, "IMPORTANT NOTICE")
  doc.setFont('times','normal')
  doc.text(283, 190, ["","", "Due to the current COVID-19 situation, if you have", "had a cough or fever or are at risk (see", "https://www.nhs.uk/conditions/coronavirus-covid-19/)", "please can you inform us immediately to cancel your", "appointment."])


  // doc.setFontSize(12)
  doc.setFont('times','normal')
  doc.text(40, 260, [moment().format('DD/MM/YYYY')], {align: "left"})

  // doc.setFontSize(11)
  doc.setFont('times','normal')
  doc.text(40, 290, ['Dear ' + current_case_object.claimant.title + ' ' + current_case_object.claimant.first_name + ' ' + current_case_object.claimant.last_name + ','], {align: "left"})
  doc.setFont('times','bold')
  doc.text(40, 310, ['RE: Your accident on ' + moment(current_case_object.accident.date).format('DD/MM/YYYY')], {align: "left"})
  doc.setFont('times','normal')
  // doc.setFontSize(10)

  var paragraph_1 = 'We are please to inform you that ' + 
                    current_case_object.instructing_party.name + 
                    ' have requested us to arrange a medical examination in connection with your personal injury claim' +
                    ' and this has been arranged as:'

  doc.text(40, 340, doc.splitTextToSize(paragraph_1, 520), {align: "left"})
  
  doc.setFont('times','bold')
  if (!adhoc){
    doc.text(40, 380, ['Expert name:                      ' + item.details.expert], {align: "left"})
    doc.text(40, 400, ['Date of appointment:         ' + moment(item.start).format('DD/MM/YYYY')], {align: "left"})
    doc.text(40, 420, ['Time of appointment:        ' + moment(item.start).format('HH:mm')], {align: "left"})
    doc.text(40, 440, doc.splitTextToSize('Venue address:                   ' + item.details.venue_detailed, 520), {align: "left"})
  }else{
    doc.text(40, 380, ['Appointment Type:            ' + item.appointment_type], {align: "left"})
    doc.text(40, 400, ['Date of appointment:         ' + moment(item.appointment_datetime).format('DD/MM/YYYY')], {align: "left"})
    doc.text(40, 420, ['Time of appointment:        ' + moment(item.appointment_datetime).format('HH:mm')], {align: "left"})
    doc.text(40, 440, doc.splitTextToSize('Venue address:                   ' + item.venue, 520), {align: "left"})
  }
  

  doc.setFont('times','normal')
  // doc.setFontSize(10)
  doc.text(40, 480, doc.splitTextToSize('For any enquiries regarding this appointment, please notify us via email on: appointments@integramedical.co.uk', 520), {align: "left"})
  doc.setFont('times','bold')
  doc.text(40, 515, doc.splitTextToSize('Please ensure that you take TWO FORMS of identification with you, one of which should include a photograph.', 520), {align: "left"})
  doc.setFont('times','normal')
  
  var paragraph_2 = 'Valid forms of identification are passport, driving licence, original birth certificate, utility bill, credit or bank card. '

  var paragraph_3 = 'Upon receipt of this letter, please would you CONFIRM your attendance of the above appointment, by either ' +
                    'e-mailing appointments@integramedical.co.uk or calling our offices.'

  doc.text(40, 550, doc.splitTextToSize(paragraph_2, 520), {align: "left"})

  doc.text(40, 585, doc.splitTextToSize(paragraph_3, 520), {align: "left"})
  doc.setFont('times','bold')
  doc.text(40, 620, doc.splitTextToSize('Please note that should you be unable to attend the above appointment you must notify us immediately by e-mail or telephone.', 520), {align: "left"})
  doc.setFont('times','normal')
  doc.text(40, 655, doc.splitTextToSize('Should you fail to notify us within 48 hours of the appointment date or you fail to attend your appointment without contacting us, a late cancellation / non-attendance fee will be charged and your solicitor will be notified.', 520), {align: "left"})
  doc.setFont('times','bold')
  doc.text(40, 700, ['Failure to attend your appointment may delay your claim.'], {align: "left"})
  doc.setFont('times','normal')
  doc.text(40, 745, ['Yours sincerely,'], {align: "left"})
  doc.text(40, 765, ['Integra Medical Reporting Ltd'], {align: "left"})

  if(return_content){
    var document_name = "Claimant Appointment Notification " + "IP Ref= " + current_case_object.instructing_party.instruction_party_reference+'.pdf'
    var document_list = []
    document_list.push(doc.output('blob'))
    document_list.push(document_name)
    console.log('content to be returned')
    return document_list
  } else {
    doc.save("Appointment Notification - Our Ref= " + our_ref + "- Solicitor's Ref= " + current_case_object.instructing_party.instruction_party_reference+'.pdf')
    window.open(doc.output('bloburl'), '_blank')
  }
}

function expertSlotRequestPDF(item, return_content, include_ranges){
  console.log(item.details.venue)
  const current_case_object = JSON.parse(sessionStorage.getItem('current_case_object'))
  var doc = new jsPDF('p', 'pt')
  let logoData = "data:image/jpg;base64,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"
  doc.setFontSize(12)
  doc.setFont('times','normal')
  doc.addImage(logoData, 'JPEG', -30, 15)

  doc.setFontSize(9)
  doc.setTextColor(150)
  doc.text(550, 40, ['Integra Medical Reporting Ltd',
                      'Building 3',
                      'Chiswick Park',
                      '566 Chiswick High Road', 
                      'Chiswick', 
                      'London', 
                      'W4 5YA',
                      'Tel: 0845 862 1909',
                      'Email: appointments@integramedical.co.uk',
                      'Website: https://www.integramedical.co.uk'
                      ], {align: "right"})

  doc.setTextColor(0, 0, 0)
  doc.setFont('times','normal')
  doc.setFontSize(12)

  var our_ref=current_case_object.claimant.last_name.substring(0,3) + current_case_object.id

  doc.text(40, 120, doc.splitTextToSize(item.details.expert_name, 520), {align: "left"})
  doc.text(40, 130, item.details.expert_address.split(', '), {align: "left"})

  var medco_id = 'N/A'
  if (current_case_object.instructing_party.medco_id){
    medco_id = current_case_object.instructing_party.medco_id
  }

  doc.setFont('times','bold')
  doc.text(40, 205, doc.splitTextToSize('Date: ' + moment().format('DD/MM/YYYY'), 520), {align: "left"})

  doc.text(40, 230, doc.splitTextToSize('Our Ref: ' + our_ref, 520), {align: "left"})
  doc.text(40, 245, doc.splitTextToSize('Solicitor Ref: ' + current_case_object.instructing_party.instruction_party_reference, 520), {align: "left"})
  doc.text(40, 260, doc.splitTextToSize('Solicitor: ' + current_case_object.instructing_party.name, 520), {align: "left"})
  doc.text(40, 275, doc.splitTextToSize('MedCo ID: ' + medco_id, 520), {align: "left"})
  doc.text(40, 290, doc.splitTextToSize('Accident Date: ' + moment(current_case_object.accident.date).format('DD/MM/YYYY'), 520), {align: "left"})

  doc.setFont('times', 'normal')
  doc.text(40, 350, doc.splitTextToSize('Dear ' + item.details.expert_name + ','), {align: "left"})
  
  doc.setFont('times','bold')
  doc.setFontSize(16)
  doc.text(300, 370, doc.splitTextToSize('New Instruction', 520), {align: "center"})

  doc.setFont('times','normal')
  doc.setFontSize(12)

  var paragraph_1 = 'Please can you arrange a suitable examination date and provide a medical report for the claimant details below that is compliant with our set Terms and Conditions.'
  doc.text(40, 400, doc.splitTextToSize(paragraph_1, 520), {align: "left"})

  var claimant_address = []
  if (current_case_object.claimant.address1){
    claimant_address.push(current_case_object.claimant.address1)
  }
  if (current_case_object.claimant.address2){
    claimant_address.push(current_case_object.claimant.address2)
  }
  if (current_case_object.claimant.address3){
    claimant_address.push(current_case_object.claimant.address3)
  }
  if (current_case_object.claimant.postcode){
    claimant_address.push(current_case_object.claimant.postcode)
  }

  var computed_body = []
  computed_body.push(
    ['Claimant', current_case_object.claimant.title + ' ' + current_case_object.claimant.first_name + ' ' + current_case_object.claimant.last_name],
    ['Litigation Friend', current_case_object.claimant.litigation_friend],
    ['D.O.B', moment(current_case_object.claimant.date_of_birth).format('DD/MM/YYYY')],
    ['Address', claimant_address],
    ['Telephone Number', current_case_object.claimant.mobile1],
    ['Email address', current_case_object.claimant.email],
    ['Appointment Venue', item.details.venue]
  )

  if (current_case_object.instructions.recommended_appointment_range_start && include_ranges){
    computed_body.push(
      ['Recommended appointment after date', moment(current_case_object.instructions.recommended_appointment_range_start).format('DD/MM/YYYY')]
    )
  }

  if (current_case_object.instructions.recommended_appointment_range_end && include_ranges){
    computed_body.push(
      ['Recommended appointment before date', moment(current_case_object.instructions.recommended_appointment_range_end).format('DD/MM/YYYY')]
    )
  }

  computed_body.push(
    ['Special Instructions', current_case_object.instructions.instructions],
    ['Records Review', current_case_object.instructing_party.records_required],
    ['Accident Type', current_case_object.accident.type],
    ['Injury Details', current_case_object.accident.injuries],
    ['Type of Report', item.details.product_name]
  )

  doc.autoTable({
    startY: 440,
    body: computed_body
  });

  doc.addPage()
  doc.setFont('times','bold')
  doc.text(40, 60, doc.splitTextToSize('Appointment', 520), {align: "left"})

  doc.setFont('times','normal')
  var paragraph_2 = 'Please contact our claimant to arrange a mutually convenient appointment. We wish to be advised of the appointment details within ' + item.details.expert_sla_instr_to_app + ' days of date of this letter via one of the following methods:'
  doc.text(40, 80, doc.splitTextToSize(paragraph_2, 520), {align: "left"})

  doc.text(40, 120, doc.splitTextToSize('Email: appointments@integramedical.co.uk', 520), {align: "left"})
  doc.text(40, 140, doc.splitTextToSize('Tel: 0845 257 5910', 520), {align: "left"})

  doc.setFont('times','bold')
  doc.text(40, 180, doc.splitTextToSize('Non Attendance', 520), {align: "left"})

  doc.setFont('times','normal')
  var paragraph_3 = 'Should the claimant fail to attend the appointment it is import you advise us within 48 hours'
  doc.text(40, 200, doc.splitTextToSize(paragraph_3, 520), {align: "left"})

  doc.setFont('times','bold')
  doc.text(40, 240, doc.splitTextToSize('Report', 520), {align: "left"})

  doc.setFont('times','normal')
  var paragraph_4 = 'A full and detailed medical report is to be produced within ' + item.details.sla_app_to_rep + ' days of the appointment date, detailing:'
  doc.text(40, 260, doc.splitTextToSize(paragraph_4, 520), {align: "left"})

  var bullet_points = [
    '• Photographic ID provided and verified',
    '• Any pre-accident medical history',
    '• Injuries sustained',
    '• Treatment received',
    '• If this incident was related to an RTA state whether the claimant was wearing a seatbelt and if not',
    '  how this may have affected the injuries',
    '• Please advise if, in your opinion, you feel our claimant should be examined by a further Medical Expert',
    '  i.e. Orthopaedic Consultant, and a medical report obtained'
  ]
  doc.text(60, 290, doc.splitTextToSize(bullet_points, 520), {align: "left"})

  var paragraph_5 = 'Please also make reference to the client’s present condition and capacity for work, concluding with an opinion and separate prognosis. Please also remark upon whether any time taken from work was reasonable and clearly state any rehabilitative treatments required, noting the number of sessions'

  doc.text(40, 430, doc.splitTextToSize(paragraph_5, 520), {align: "left"})

  doc.setFont('times','bold')
  doc.text(40, 470, doc.splitTextToSize('Please contact us immediately, should you feel unable to meet any of the above conditions.', 520), {align: "left"})

  doc.text(40, 500, doc.splitTextToSize('Please email your report to reports@integramedical.co.uk', 520), {align: "left"})

  doc.text(40, 530, doc.splitTextToSize('At the end of the report the following MUST be stated:', 520), {align: "left"})

  var paragraph_6 = 'I confirm that I understood my duty to the court and have complied with and will continue to comply with it. I also confirm that I am aware of the requirements of CRP Part 35, Practice Direction 35 the protocol for the instruction of experts to give evident in Civil Claims and the Practice Direction on pre-action conduct.'

  doc.setFont('times','normal')
  doc.text(40, 550, doc.splitTextToSize(paragraph_6, 520), {align: "left"})

  var paragraph_7 = 'In order to comply with the court rules, please ensure that the report contains a Statement of Truth, before the signature and date. This may resemble “I confirm that I have made clear which facts and matters referred to in this report are within my own knowledge and which are not. Those that are within my own knowledge I confirm to be true. The opinions I have expressed represent my true and complete professional opinions on the matters to which they refer.” An expert’s report should be addressed “ to the Court”.'

  doc.text(40, 610, doc.splitTextToSize(paragraph_7, 520), {align: "left"})

  doc.setFont('times','bold')
  var paragraph_8 = 'Please do not carry out any x-rays or other diagnostic investigations, without prior authorisation from Integra Medical Reporting.'

  doc.text(40, 700, doc.splitTextToSize(paragraph_8, 520), {align: "left"})

  doc.setFont('times','normal')
  var paragraph_9 = 'Should you believe that your charge for this report should be higher than our agreed fee, please advise us immediately, in order that we may inform and discuss this with the necessary Solicitor/ Insurer.'
  doc.text(40, 740, doc.splitTextToSize(paragraph_9, 520), {align: "left"})

  doc.addPage()

  doc.setFont('times', 'bold')
  doc.text(40, 60, ['Medical records'], {align: "left"})
  
  doc.setFont('times', 'normal')
  doc.text(40, 80, doc.splitTextToSize('Should any medical records have been supplied with this instruction, please do not return them unless specifically requested but instead securely destroy them.', 520), {align: "left"})

  doc.setFont('times', 'bold')
  doc.text(40, 120, ['Conflict of interest'], {align: "left"})
  
  doc.setFont('times', 'normal')
  doc.text(40, 140, doc.splitTextToSize('In the event the client is known to you, such as a family member, friend, work colleague, or patient please cancel this instruction and inform us immediately.', 520), {align: "left"})

  doc.text(40, 220, doc.splitTextToSize('Yours faithfully,', 520), {align: "left"})
  doc.text(40, 240, doc.splitTextToSize('Integra Medical Reporting', 520), {align: "left"})


  if(return_content){
    var document_name = "Expert Appointment Slot Request " + "IP Ref= " + current_case_object.instructing_party.instruction_party_reference+'.pdf'
    var document_list = []
    document_list.push(doc.output('blob'))
    document_list.push(document_name)
    console.log('content to be returned')
    return document_list
  } else {
    doc.save("Expert Appointment Slot Request - Our Ref= " + our_ref + "- Solicitor's Ref= " + current_case_object.instructing_party.instruction_party_reference+'.pdf')
    window.open(doc.output('bloburl'), '_blank')
  }
}

function expertAppointmentNotificationPDF(item, return_content){
  const current_case_object = JSON.parse(sessionStorage.getItem('current_case_object'))
  var doc = new jsPDF('p', 'pt')
  let logoData = "data:image/jpg;base64,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"
  doc.setFontSize(12)
  doc.setFont('times','normal')
  doc.addImage(logoData, 'JPEG', -30, 15)

  doc.setFontSize(9)
  doc.setTextColor(150)
  doc.text(550, 40, ['Integra Medical Reporting Ltd',
                      'Building 3',
                      'Chiswick Park',
                      '566 Chiswick High Road', 
                      'Chiswick', 
                      'London', 
                      'W4 5YA',
                      'Tel: 0845 862 1909',
                      'Email: appointments@integramedical.co.uk',
                      'Website: https://www.integramedical.co.uk'
                      ], {align: "right"})

  doc.setTextColor(0, 0, 0)
  doc.setFont('times','normal')
  doc.setFontSize(12)

  var our_ref=current_case_object.claimant.last_name.substring(0,3) + current_case_object.id

  doc.text(40, 120, doc.splitTextToSize(item.details.expert_details.name, 520), {align: "left"})
  doc.text(40, 130, item.details.expert_details.address.split(', '), {align: "left"})

  doc.setFont('times','bold')

  var medco_id = 'N/A'
  if (current_case_object.instructing_party.medco_id){
    medco_id = current_case_object.instructing_party.medco_id
  }
  doc.text(40, 205, doc.splitTextToSize('Date: ' + moment().format('DD/MM/YYYY'), 520), {align: "left"})

  doc.text(40, 230, doc.splitTextToSize('Our Ref: ' + our_ref, 520), {align: "left"})
  doc.text(40, 245, doc.splitTextToSize('Solicitor Ref: ' + current_case_object.instructing_party.instruction_party_reference, 520), {align: "left"})
  doc.text(40, 260, doc.splitTextToSize('Solicitor: ' + current_case_object.instructing_party.name, 520), {align: "left"})
  doc.text(40, 275, doc.splitTextToSize('MedCo ID: ' + medco_id, 520), {align: "left"})
  doc.text(40, 290, doc.splitTextToSize('Accident Date: ' + moment(current_case_object.accident.date).format('DD/MM/YYYY'), 520), {align: "left"})

  doc.setFont('times', 'normal')
  doc.text(40, 350, doc.splitTextToSize('Dear ' + item.details.expert_details.name + ','), {align: "left"})
  
  doc.setFont('times','bold')
  doc.setFontSize(16)
  doc.text(300, 370, doc.splitTextToSize('New Instruction', 520), {align: "center"})

  doc.setFont('times','normal')
  doc.setFontSize(12)

  var paragraph_1 = 'Please find below the details for the BOOKED appointment and claimant and provide a medical report for the claimant details that is compliant with our set Terms and Conditions.'
  doc.text(40, 400, doc.splitTextToSize(paragraph_1, 520), {align: "left"})

  var claimant_address = []
  if (current_case_object.claimant.address1){
    claimant_address.push(current_case_object.claimant.address1)
  }
  if (current_case_object.claimant.address2){
    claimant_address.push(current_case_object.claimant.address2)
  }
  if (current_case_object.claimant.address3){
    claimant_address.push(current_case_object.claimant.address3)
  }
  if (current_case_object.claimant.postcode){
    claimant_address.push(current_case_object.claimant.postcode)
  }

  doc.autoTable({
    startY: 440,
    body: [
        ['Claimant', current_case_object.claimant.title + ' ' + current_case_object.claimant.first_name + ' ' + current_case_object.claimant.last_name],
        ['Litigation Friend', current_case_object.claimant.litigation_friend],
        ['D.O.B', moment(current_case_object.claimant.date_of_birth).format('DD/MM/YYYY')],
        ['Address', claimant_address],
        ['Telephone Number', current_case_object.claimant.mobile1],
        ['Email address', current_case_object.claimant.email],
        ['Appointment Venue', item.details.venue_detailed],
        ['Appointment Date', moment(item.start).format('DD/MM/YYYY')],
        ['Appointment Time', moment(item.start).format('HH:mm')],
        ['Special Instructions', current_case_object.instructions.instructions],
        ['Records Review', current_case_object.instructing_party.records_required],
        ['Accident Type', current_case_object.accident.type],
        ['Injury Details', current_case_object.accident.injuries],
        ['Type of Report', item.details.product_name]
    ]
  });

  doc.addPage()
  doc.setFont('times','bold')
  doc.text(40, 60, doc.splitTextToSize('Appointment', 520), {align: "left"})

  doc.setFont('times','normal')
  var paragraph_2 = 'Please contact our claimant to arrange a mutually convenient appointment. We wish to be advised of the appointment details within ' + item.details.expert_sla_instr_to_app + ' days of date of this letter via one of the following methods:'
  doc.text(40, 80, doc.splitTextToSize(paragraph_2, 520), {align: "left"})

  doc.text(40, 120, doc.splitTextToSize('Email: appointments@integramedical.co.uk', 520), {align: "left"})
  doc.text(40, 140, doc.splitTextToSize('Tel: 0845 257 5910', 520), {align: "left"})

  doc.setFont('times','bold')
  doc.text(40, 180, doc.splitTextToSize('Non Attendance', 520), {align: "left"})

  doc.setFont('times','normal')
  var paragraph_3 = 'Should the claimant fail to attend the appointment it is import you advise us within 48 hours'
  doc.text(40, 200, doc.splitTextToSize(paragraph_3, 520), {align: "left"})

  doc.setFont('times','bold')
  doc.text(40, 240, doc.splitTextToSize('Report', 520), {align: "left"})

  doc.setFont('times','normal')
  var paragraph_4 = 'A full and detailed medical report is to be produced within ' + item.details.expert_details.sla_app_to_rep + ' days of the appointment date, detailing:'
  doc.text(40, 260, doc.splitTextToSize(paragraph_4, 520), {align: "left"})

  var bullet_points = [
    '• Photographic ID provided and verified',
    '• Any pre-accident medical history',
    '• Injuries sustained',
    '• Treatment received',
    '• If this incident was related to an RTA state whether the claimant was wearing a seatbelt and if not',
    '  how this may have affected the injuries',
    '• Please advise if, in your opinion, you feel our claimant should be examined by a further Medical Expert',
    '  i.e. Orthopaedic Consultant, and a medical report obtained'
  ]
  doc.text(60, 290, doc.splitTextToSize(bullet_points, 520), {align: "left"})

  var paragraph_5 = 'Please also make reference to the client’s present condition and capacity for work, concluding with an opinion and separate prognosis. Please also remark upon whether any time taken from work was reasonable and clearly state any rehabilitative treatments required, noting the number of sessions'

  doc.text(40, 430, doc.splitTextToSize(paragraph_5, 520), {align: "left"})

  doc.setFont('times','bold')
  doc.text(40, 470, doc.splitTextToSize('Please contact us immediately, should you feel unable to meet any of the above conditions.', 520), {align: "left"})

  doc.text(40, 500, doc.splitTextToSize('Please email your report to reports@integramedical.co.uk', 520), {align: "left"})

  doc.text(40, 530, doc.splitTextToSize('At the end of the report the following MUST be stated:', 520), {align: "left"})

  var paragraph_6 = 'I confirm that I understood my duty to the court and have complied with and will continue to comply with it. I also confirm that I am aware of the requirements of CRP Part 35, Practice Direction 35 the protocol for the instruction of experts to give evident in Civil Claims and the Practice Direction on pre-action conduct.'

  doc.setFont('times','normal')
  doc.text(40, 550, doc.splitTextToSize(paragraph_6, 520), {align: "left"})

  var paragraph_7 = 'In order to comply with the court rules, please ensure that the report contains a Statement of Truth, before the signature and date. This may resemble “I confirm that I have made clear which facts and matters referred to in this report are within my own knowledge and which are not. Those that are within my own knowledge I confirm to be true. The opinions I have expressed represent my true and complete professional opinions on the matters to which they refer.” An expert’s report should be addressed “ to the Court”.'

  doc.text(40, 610, doc.splitTextToSize(paragraph_7, 520), {align: "left"})

  doc.setFont('times','bold')
  var paragraph_8 = 'Please do not carry out any x-rays or other diagnostic investigations, without prior authorisation from Integra Medical Reporting.'

  doc.text(40, 700, doc.splitTextToSize(paragraph_8, 520), {align: "left"})

  doc.setFont('times','normal')
  var paragraph_9 = 'Should you believe that your charge for this report should be higher than our agreed fee, please advise us immediately, in order that we may inform and discuss this with the necessary Solicitor/ Insurer.'
  doc.text(40, 740, doc.splitTextToSize(paragraph_9, 520), {align: "left"})

  doc.addPage()

  doc.setFont('times', 'bold')
  doc.text(40, 60, ['Medical records'], {align: "left"})
  
  doc.setFont('times', 'normal')
  doc.text(40, 80, doc.splitTextToSize('Should any medical records have been supplied with this instruction, please do not return them unless specifically requested but instead securely destroy them.', 520), {align: "left"})

  doc.setFont('times', 'bold')
  doc.text(40, 120, ['Conflict of interest'], {align: "left"})
  
  doc.setFont('times', 'normal')
  doc.text(40, 140, doc.splitTextToSize('In the event the client is known to you, such as a family member, friend, work colleague, or patient please cancel this instruction and inform us immediately.', 520), {align: "left"})

  doc.text(40, 220, doc.splitTextToSize('Yours faithfully,', 520), {align: "left"})
  doc.text(40, 240, doc.splitTextToSize('Integra Medical Reporting', 520), {align: "left"})


  if(return_content){
    var document_name = "Expert Appointment Booking Letter " + "IP Ref= " + current_case_object.instructing_party.instruction_party_reference+'.pdf'
    var document_list = []
    document_list.push(doc.output('blob'))
    document_list.push(document_name)
    console.log('content to be returned')
    return document_list
  } else {
    doc.save("Expert Appointment Booking Letter - Our Ref= " + our_ref + "- Solicitor's Ref= " + current_case_object.instructing_party.instruction_party_reference+'.pdf')
    window.open(doc.output('bloburl'), '_blank')
  }
}

function cleanupMarkers(){
  if(window.venueMarkers){
      for (var i = 0; i < window.venueMarkers.length; i++) {
      window.venueMarkers[i].setMap(null);
    }
  }
  window.venueMarkers = [];

  if(window.centerMarkers){
      for (var i = 0; i < window.centerMarkers.length; i++) {
      window.centerMarkers[i].setMap(null);
    }
  }
  window.centerMarkers = [];
}

function populateMap(){
    const current_case_object = JSON.parse(sessionStorage.getItem('current_case_object'))
    // HACKY WAY OF SHOWING 12 MONTHS
    var events = $("#fullCalendar").fullCalendar("clientEvents");
                 $("#fullCalendar").fullCalendar("clientEvents");
                //  $("#fullCalendar").fullCalendar("clientEvents");
                //  $("#fullCalendar").fullCalendar("clientEvents");
                //  $("#fullCalendar").fullCalendar("clientEvents");
                //  $("#fullCalendar").fullCalendar("clientEvents");
                //  $("#fullCalendar").fullCalendar("clientEvents");
                //  $("#fullCalendar").fullCalendar("clientEvents");
                //  $("#fullCalendar").fullCalendar("clientEvents");
                //  $("#fullCalendar").fullCalendar("clientEvents");
                //  $("#fullCalendar").fullCalendar("clientEvents");
                //  $("#fullCalendar").fullCalendar("clientEvents");
    events.sort((a, b) => (a.start > b.start) ? 1 : -1)
    if (!document.getElementById("venueLocationsMap") || events.length == 0){
      NProgress.done()
      cleanupMarkers()
      const currentCaseMarker = new window.google.maps.Marker({
        position: {
          lat: parseFloat(current_case_object.longlat[0]),
          lng: parseFloat(current_case_object.longlat[1])
        },
        title: current_case_object.label,
        map: window.venuesMap,
        // icon: 'https://maps.google.com/mapfiles/kml/paddle/blu-blank.png'
        icon:{
          url: 'http://maps.google.com/mapfiles/ms/micons/man.png',
          scaledSize: new google.maps.Size(30, 30)
        }
      });

      window.venueMarkers.push(currentCaseMarker)

      window.venuesMap.setCenter({
        lat: parseFloat(current_case_object.longlat[0]),
        lng: parseFloat(current_case_object.longlat[1])
      });
      if (window.slaRadius)
        delete window.slaRadius

      // var radius = 16093
      var radius = 16093/10 * 10
      if (window.sla_radius){
        radius = (16093/10) * window.sla_radius
      }

      var slaRadius = new google.maps.Circle({
        map: window.venuesMap,
        radius: radius,    // 10 miles in metres
        fillColor: '#AA0000',
        // draggable:true
      });
      slaRadius.bindTo('center', currentCaseMarker, 'position');

      window.venuesMap.setCenter({
        lat: parseFloat(current_case_object.longlat[0]),
        lng: parseFloat(current_case_object.longlat[1])
      });
      window.venueMarkers.push(slaRadius)
      window.slaRadius = slaRadius
      const selected_supported_product = sessionStorage.getItem('selected_supported_product')
      // if (selected_supported_product){
      //   Swal.fire({
      //     type: 'warning',
      //     title: 'No slots were found',
      //     html: '<b>Trying fetching some slots or increase the radius for the Question marks to show up!</b>'
      //   })
      // }
      return;
    }
    
    cleanupMarkers()

    /*
    Group events by the post code:
    */
    var eventsToPostcode = new Map();
    console.log('events', events)
    window.reset_slots_counters()
    for (var i = 0; i < events.length; i++) {
      if (events[i].id && events[i].details.external_id){
        window.increment_easyslot_slots_counter()
      }else if(events[i].id){
        window.increment_internal_slots_counter()
      }
      if(!eventsToPostcode.has(events[i].postcode.replace(' ', ''))){
        eventsToPostcode.set(events[i].postcode.replace(' ', ''), [])
      }
      eventsToPostcode.get(events[i].postcode.replace(' ', '')).push(events[i])
    }
    console.log('eventsToPostcode', eventsToPostcode)

    eventsToPostcode.forEach((events, postcode, _m_) => {
      //CHECK IF IT HAS ID AS WELL
        var today = new Date()
        if(events[0].longlat && events[0].id){
          var event_day = moment(new Date(events[0].start))
          var now = moment(new Date())
          var calendar_days = moment.duration(event_day.diff(now, 'days'));
          const marker = new window.google.maps.Marker({
              position: {
                lat: parseFloat(events[0].longlat[0]),
                lng: parseFloat(events[0].longlat[1])
              },
              title: calendar_days + ' Calendar Days Ahead: [' + events[0].postcode + ']',
              map: window.venuesMap,
              icon: {
                url: 'http://maps.google.com/mapfiles/ms/icons/green-dot.png',
                scaledSize: new google.maps.Size(50, 50)
              },
              // draggable:true
            });
          
          marker.events = events
          marker.addListener('click', function() {
              var dialog_content = '<div class="md-field md-theme-default"><div class="md-layout md-size-100">'
              var eventsToVenue = new Map();
              console.log('this.events', this.events)
              for (var i = 0; i < this.events.length; i++) {
                if(!eventsToVenue.has(this.events[i].details.postcode.replace(' ', ''))){
                  eventsToVenue.set(this.events[i].details.postcode.replace(' ', ''), [])
                }
                eventsToVenue.get(this.events[i].details.postcode.replace(' ', '')).push(this.events[i])
              }
              eventsToVenue.forEach((_events_for_venue_, venue, _m_) => {
                dialog_content += '<div class="md-layout-item md-size-100">Venue: '+ _events_for_venue_[0].details.venue+'</div>'
                // _events_for_venue_.sort((a, b) => (a.start > b.start) ? 1 : -1)
                  for (var i = 0; i < _events_for_venue_.length; i++) {
                    var reserved_span = ''
                    if (_events_for_venue_[i].id && events[i].details.external_id){
                      if (_events_for_venue_[i].reserved_by){
                        reserved_span = "<span style='color: red;'>Reserved by: " + _events_for_venue_[i].reserved_by + "</span>"
                      }
                      console.log(events[i].details.external_id)
                      dialog_content += '<div class="md-layout-item md-size-100">' + 
                        '<input type="radio" style="display:inline-block;vertical-align:middle;" class="md-radio" name="map_dialog_book_slot_radio" value="'+events[i].id+','+events[i].details.external_id+'">'+
                          _events_for_venue_[i].start.format('DD-MM-YYYY HH:mm') + ' : ' +
                          _events_for_venue_[i].details.expert +
                          ' [Easyslot] ' + `[${_events_for_venue_[i].details.venue}] ${reserved_span}` +
                        '</input>' +
                      '</div>'                        
                    }else if(_events_for_venue_[i].id){
                      var reserved_span = ''
                      if (_events_for_venue_[i].reserved_by){
                        reserved_span = "<span style='color: red;'>Reserved by: " + _events_for_venue_[i].reserved_by + "</span>"
                      }
                      dialog_content += '<div class="md-layout-item md-size-100">' + 
                        '<input type="radio" style="display:inline-block;vertical-align:middle;" class="md-radio" name="map_dialog_book_slot_radio" value="'+events[i].id+'">'+
                          _events_for_venue_[i].start.format('DD-MM-YYYY HH:mm') + ' : ' +
                          _events_for_venue_[i].details.expert + 
                          ' [Internal] ' + `[${_events_for_venue_[i].details.venue}] ${reserved_span}` +
                        '</input>' +
                      '</div>' 

                    }
                  }
                }
              )
              var selected_slot = null
              var slot_external_id = null
              var booking_form_data_note = null
              var booking_form_data_email_list = []
              var booking_form_data_additional_emails = null
              var delay_reasons = []
              dialog_content += '</div></div>'

              var booked_with_claimant = false
              var booked_with_instructing_party = false
              var booked_with_no_one = false
              
              Swal.mixin({
                confirmButtonText: 'Next &rarr;',
                showCancelButton: true,
                progressSteps: ['1', '2'],
                width: '1200px',
              }).queue([
                {
                  title: "Available slots at " + this.events[0].postcode,
                  html: dialog_content,
                  showCancelButton: true,
                  confirmButtonClass: "md-button md-success",
                  cancelButtonClass: "md-button md-danger",
                  buttonsStyling: true,
                  customClass: 'swal-wide',
                  preConfirm: () => {
                  document.getElementsByName('map_dialog_book_slot_radio').forEach(element => {
                    if(element.checked){
                      if (element.value.includes(',')){
                        console.log(element.value)
                        selected_slot = Number(element.value.split(',')[0])
                        slot_external_id = element.value.split(',')[1]
                      }else{
                        selected_slot = Number(element.value)
                        slot_external_id = null
                      }
                    }
                  });
                  console.log('external id: ', slot_external_id)
                  console.log(selected_slot)
                  $http
                      .post(window.url__appointment_reserve_slot, {'slot_id': selected_slot})
                      .then(response => {
                        console.log('Slot assigned to user!')                        
                      })
                      .catch(function(error) {
                          console.error(error.response);
                      })
                  }
                },
                {
                  title: "A bit more details!",                 
                  html: '<div class="md-layout-item md-size-100" style="text-align: left">'
                        +'<label style="font-size: 20px;">Additional emails seperated by a ,</label>'
                        +'<div class="md-field md-theme-default md-has-value md-has-textarea">'
                        +  '<textarea style="border-style: solid; border-width: 1px" data-vv-name="item.other" id="cal_dialog_book_slot_additional_emails" class="md-textarea">'
                        +  '</textarea>'
                        +'</div>'
                        + '<br>'
                        +'<div class="md-layout-item md-size-100">'
                        +'<input style="display:inline-block;vertical-align:middle;" type="checkbox" class="md-checkbox" name="who_to_email_checkboxes" value="email_claimant" checked>'
                        +'<label style="font-size: 20px"><b>Email Claimant</b></label>'
                        +'</input>'
                        +'</div>'
                        +'<div class="md-layout-item md-size-100">'
                        +'<input style="display:inline-block;vertical-align:middle;" type="checkbox" class="md-checkbox" name="who_to_email_checkboxes" value="email_instructing_party" checked>'
                        +'<label style="font-size: 20px"><b>Email Instructing Party File Handler</b></label>'
                        +'</input>'
                        +'</div>'
                        +'<div class="md-layout-item md-size-100">'
                        +'<input style="display:inline-block;vertical-align:middle;" type="checkbox" class="md-checkbox" name="who_to_email_checkboxes" value="email_expert" checked>'
                        +'<label style="font-size: 20px"><b>Email Expert</b></label>'
                        +'</input>'
                        +'</div>'
                        + '<div style="text-align:center;" class="md-layout-item md-size-100">'
                        + '<span style="font-size: 50px; color: red"">*** ATTENTION ***</span>'
                        + '<br>'
                        + '<span style="font-size: 40px; color: red"">SELECT ONE OF THE FOLLOWING</span>'
                        +'</div>'
                        +'<div class="md-layout-item md-size-100">'
                        +'<input style="display:inline-block;vertical-align:middle;" type="checkbox" class="md-checkbox" id="booked_with_claimant" value="true">'
                        +'<label style="font-size: 35px"><b><u>Booked with claimant</u></b></label>'
                        +'</input>'
                        +'</div>'
                        +'<div class="md-layout-item md-size-100">'
                        +'<input style="display:inline-block;vertical-align:middle;" type="checkbox" class="md-checkbox" id="booked_with_instructing_party" value="true">'
                        +'<label style="font-size: 35px"><b><u>Booked with IP</u></b></label>'
                        +'</input>'
                        +'</div>'
                        +'<div class="md-layout-item md-size-100">'
                        +'<input style="display:inline-block;vertical-align:middle;" type="checkbox" class="md-checkbox" id="booked_without_any_claimant_contact" value="true">'
                        +'<label style="font-size: 35px"><b><u>Booked without any Claimant contact</u></b></label>'
                        +'</input>'
                        +'</div>'
                        +'<div class="md-layout-item md-size-100">'
                        +'<br>'
                        + '<label for="map_dialog_book_slot_note" style="font-size: 20px;">Appointment Notes</label>'
                        +   '<div class="md-field md-theme-default md-has-value md-has-textarea">'
                        +     '<textarea style="border-style: solid; border-width: 1px" id="map_dialog_book_slot_note" class="md-textarea">'
                        +     '</textarea>'
                        +   '</div>'
                        +'</div>',
                  showCancelButton: true,
                  confirmButtonClass: "md-button md-success",
                  confirmButtonText: "Book it",
                  cancelButtonClass: "md-button md-danger",
                  buttonsStyling: true,
                  preConfirm: () => {
                    booking_form_data_note = document.getElementById('map_dialog_book_slot_note').value
                    booking_form_data_additional_emails = document.getElementById('cal_dialog_book_slot_additional_emails').value
                    document.getElementsByName('who_to_email_checkboxes').forEach(element => {
                    if(element.checked){
                      booking_form_data_email_list.push(element.value)
                      }
                    });
                    if (document.getElementById('booked_with_claimant').checked){
                      booked_with_claimant = true;
                    }
                    if (document.getElementById('booked_with_instructing_party').checked){
                      booked_with_instructing_party = true;
                    }
                    if (document.getElementById('booked_without_any_claimant_contact').checked){
                      booked_with_no_one = true;
                    }
                  }
                
                }
              ]).then(result => {
                if (result.value && selected_slot ) {
                  $http
                      .post(window.url__appointment_exceeding_sla, {'slot_id': selected_slot, 'case_id': current_case_object.id})
                      .then(response => {
                          if (response.data.exceeded){
                            Swal.fire({
                              title: 'Exceeding SLA',
                              html: '<div><label style="font-size: 150px; color: red">' + response.data.days + '</label><h3>Business Days<br><u>Instruction Date &rarr; Appointment Date</u></h3></div>',
                              type: 'warning',
                              showCancelButton: true,
                              confirmButtonColor: '#3085d6',
                              cancelButtonColor: '#d33',
                              confirmButtonText: 'Yes, go ahead!'
                            }).then((result) => {
                              if (result.value) {
                                Swal.fire({
                                title: "Reason for Exceeding the SLA",
                                width: 1200,
                                animation: false,
                                html:   '<div class="md-layout-item md-size-100" style="text-align: left">'
                                        +'<input type="checkbox" style="display:inline-block;vertical-align:middle;" class="md-checkbox" name="reasons_checkboxes" value="[ip delayed via phone]">'
                                        +'<label>IP Delayed via Phone</label>'
                                        +'</input>'
                                        +'</div>'
                                        +'<div class="md-layout-item md-size-100" style="text-align: left">'
                                        +'<input type="checkbox" style="display:inline-block;vertical-align:middle;" class="md-checkbox" name="reasons_checkboxes" value="[ip delayed via email]">'
                                        +'<label>IP Delayed via Email</label>'
                                        +'</input>'
                                        +'</div>'
                                        +'<div class="md-layout-item md-size-100" style="text-align: left">'
                                        +'<input type="checkbox" style="display:inline-block;vertical-align:middle;" class="md-checkbox" name="reasons_checkboxes" value="[claimant delayed via phone]">'
                                        +'<label>Claimant Delayed via Phone</label>'
                                        +'</input>'
                                        +'</div>'
                                        +'<div class="md-layout-item md-size-100" style="text-align: left">'
                                        +'<input type="checkbox" style="display:inline-block;vertical-align:middle;" class="md-checkbox" name="reasons_checkboxes" value="[claimant delayed via email]">'
                                        +'<label>Claimant Delayed via Email</label>'
                                        +'</input>'
                                        +'</div>'
                                        +'<div class="md-layout-item md-size-100" style="text-align: left">'
                                        +'<input type="checkbox" style="display:inline-block;vertical-align:middle;" class="md-checkbox" name="reasons_checkboxes" value="[claimant dnad]">'
                                        +"<label>Claimant DNAD</label>"
                                        +'</input>'
                                        +'</div>'
                                        +'<div class="md-layout-item md-size-100" style="text-align: left">'
                                        +'<input type="checkbox" style="display:inline-block;vertical-align:middle;" class="md-checkbox" name="reasons_checkboxes" value="[claimant re-arranged]">'
                                        +"<label>Claimant Re-arranged</label>"
                                        +'</input>'
                                        +'</div>'
                                        +'<div class="md-layout-item md-size-100" style="text-align: left">'
                                        +'<input type="checkbox" style="display:inline-block;vertical-align:middle;" class="md-checkbox" name="reasons_checkboxes" value="[ip re-arranged]">'
                                        +"<label>IP Re-arranged</label>"
                                        +'</input>'
                                        +'</div>'
                                        +'<div class="md-layout-item md-size-100" style="text-align: left">'
                                        +'<input type="checkbox" style="display:inline-block;vertical-align:middle;" class="md-checkbox" name="reasons_checkboxes" value="[agency re-arranged]">'
                                        +"<label>Agency Re-arranged</label>"
                                        +'</input>'
                                        +'</div>'
                                        +'<div class="md-layout-item md-size-100" style="text-align: left">'
                                        +'<input type="checkbox" style="display:inline-block;vertical-align:middle;" class="md-checkbox" name="reasons_checkboxes" value="[clinic cancelled]">'
                                        +"<label>Clinic Cancelled</label>"
                                        +'</input>'
                                        +'</div>'
                                        +'<div class="md-layout-item md-size-100" style="text-align: left">'
                                        +'<input type="checkbox" style="display:inline-block;vertical-align:middle;" class="md-checkbox" name="reasons_checkboxes" value="[case cancelled]">'
                                        +"<label>Case Cancelled</label>"
                                        +'</input>'
                                        +'</div>'
                                        +'<div class="md-layout-item md-size-100" style="text-align: left">'
                                        +'<input type="checkbox" style="display:inline-block;vertical-align:middle;" class="md-checkbox" name="reasons_checkboxes" value="[no show]">'
                                        +'<label>No Show</label>'
                                        +'</input>'
                                        +'</div>'
                                        +'<div class="md-layout-item md-size-100" style="text-align: left">'
                                        +'<input type="checkbox" style="display:inline-block;vertical-align:middle;" class="md-checkbox" name="reasons_checkboxes" value="[abandoned]">'
                                        +'<label>Abandoned</label>'
                                        +'</input>'
                                        +'</div>'
                                        +'<div class="md-layout-item md-size-100" style="text-align: left">'
                                        +'<input type="checkbox" style="display:inline-block;vertical-align:middle;" class="md-checkbox" name="reasons_checkboxes" value="[on hold by ip]">'
                                        +'<label>On Hold by IP</label>'
                                        +'</input>'
                                        +'</div>'
                                        +'<div class="md-layout-item md-size-100" style="text-align: left">'
                                        +'<input type="checkbox" style="display:inline-block;vertical-align:middle;" class="md-checkbox" name="reasons_checkboxes" value="[on hold by agency]">'
                                        +'<label>On Hold by Agency</label>'
                                        +'</input>'
                                        +'</div>'
                                        +'<br>'
                                        +'<div class="md-layout-item md-size-100" style="text-align: left">'
                                        +'<input type="checkbox" style="display:inline-block;vertical-align:middle;" class="md-checkbox" name="reasons_checkboxes" value="[other]">'
                                        +'<label>Other</label>'
                                        +'</input>'
                                        +'</div>'
                                        +'<br>'
                                        +'<div class="md-layout-item md-size-100" style="text-align: left">'
                                        +'<label style="font-size: 20px;">Exceeding SLA Notes</label>'
                                        +'<div class="md-field md-theme-default md-has-value md-has-textarea">'
                                        +  '<textarea style="border-style: solid; border-width: 1px" data-vv-name="item.other" id="cal_dialog_book_slot_note" class="md-textarea">'
                                        +  '</textarea>'
                                        +'</div>'
                                        +'</div>',
                                        showCancelButton: true,
                                        showCloseButton: true,
                                        confirmButtonClass: "md-button md-success",
                                        confirmButtonText: "Proceed",
                                        cancelButtonClass: "md-button md-danger",
                                        buttonsStyling: true,
                                        preConfirm: () => {
                                          booking_form_data_note += ' Exceeding SLA Notes: ' + document.getElementById('cal_dialog_book_slot_note').value
                                          document.getElementsByName('reasons_checkboxes').forEach(element => {
                                          if (element.checked){
                                              delay_reasons.push(element.value)
                                          }                 
                                          });
                                          console.log('delay_reasons', delay_reasons) 
                                        }
                                }).then((result) => {
                                  if (result.value) {
                                    if (booking_form_data_note){
                                      booking_form_data_note += ', ' + delay_reasons.join()
                                    }else{
                                      booking_form_data_note = delay_reasons.join()
                                    }
                                    window.book_slot(this.events, selected_slot, slot_external_id, booking_form_data_note, booking_form_data_email_list, booking_form_data_additional_emails, booked_with_claimant, booked_with_instructing_party, booked_with_no_one)
                                    return
                                  }
                                })
                              }
                            })
                          }else{
                            Swal.fire({
                              title: 'Appointment SLA',
                              html: '<div><label style="font-size: 150px; color: green">' + response.data.days + '</label><h3>Business Days<br><u>Instruction Date &rarr; Appointment Date</u></h3></div>',
                              type: 'success',
                              showCancelButton: true,
                              confirmButtonColor: '#3085d6',
                              cancelButtonColor: '#d33',
                              confirmButtonText: 'Proceed!'
                            }).then((result) => {
                              if (result.value) {
                                Swal.fire({
                                title: "Reason for Booking this Appointment",
                                width: 1200,
                                animation: false,
                                html:   '<div class="md-layout-item md-size-100" style="text-align: left">'
                                        +'<input type="checkbox" style="display:inline-block;vertical-align:middle;" class="md-checkbox" name="reasons_checkboxes" value="[ip delayed via phone]">'
                                        +'<label>IP Delayed via Phone</label>'
                                        +'</input>'
                                        +'</div>'
                                        +'<div class="md-layout-item md-size-100" style="text-align: left">'
                                        +'<input type="checkbox" style="display:inline-block;vertical-align:middle;" class="md-checkbox" name="reasons_checkboxes" value="[ip delayed via email]">'
                                        +'<label>IP Delayed via Email</label>'
                                        +'</input>'
                                        +'</div>'
                                        +'<div class="md-layout-item md-size-100" style="text-align: left">'
                                        +'<input type="checkbox" style="display:inline-block;vertical-align:middle;" class="md-checkbox" name="reasons_checkboxes" value="[claimant delayed via phone]">'
                                        +'<label>Claimant Delayed via Phone</label>'
                                        +'</input>'
                                        +'</div>'
                                        +'<div class="md-layout-item md-size-100" style="text-align: left">'
                                        +'<input type="checkbox" style="display:inline-block;vertical-align:middle;" class="md-checkbox" name="reasons_checkboxes" value="[claimant delayed via email]">'
                                        +'<label>Claimant Delayed via Email</label>'
                                        +'</input>'
                                        +'</div>'
                                        +'<div class="md-layout-item md-size-100" style="text-align: left">'
                                        +'<input type="checkbox" style="display:inline-block;vertical-align:middle;" class="md-checkbox" name="reasons_checkboxes" value="[claimant dnad]">'
                                        +"<label>Claimant DNAD</label>"
                                        +'</input>'
                                        +'</div>'
                                        +'<div class="md-layout-item md-size-100" style="text-align: left">'
                                        +'<input type="checkbox" style="display:inline-block;vertical-align:middle;" class="md-checkbox" name="reasons_checkboxes" value="[claimant re-arranged]">'
                                        +"<label>Claimant Re-arranged</label>"
                                        +'</input>'
                                        +'</div>'
                                        +'<div class="md-layout-item md-size-100" style="text-align: left">'
                                        +'<input type="checkbox" style="display:inline-block;vertical-align:middle;" class="md-checkbox" name="reasons_checkboxes" value="[ip re-arranged]">'
                                        +"<label>IP Re-arranged</label>"
                                        +'</input>'
                                        +'</div>'
                                        +'<div class="md-layout-item md-size-100" style="text-align: left">'
                                        +'<input type="checkbox" style="display:inline-block;vertical-align:middle;" class="md-checkbox" name="reasons_checkboxes" value="[agency re-arranged]">'
                                        +"<label>Agency Re-arranged</label>"
                                        +'</input>'
                                        +'</div>'
                                        +'<div class="md-layout-item md-size-100" style="text-align: left">'
                                        +'<input type="checkbox" style="display:inline-block;vertical-align:middle;" class="md-checkbox" name="reasons_checkboxes" value="[case cancelled]">'
                                        +"<label>Case Cancelled</label>"
                                        +'</input>'
                                        +'</div>'
                                        +'<div class="md-layout-item md-size-100" style="text-align: left">'
                                        +'<input type="checkbox" style="display:inline-block;vertical-align:middle;" class="md-checkbox" name="reasons_checkboxes" value="[clinic cancelled]">'
                                        +"<label>Clinic Cancelled</label>"
                                        +'</input>'
                                        +'</div>'
                                        +'<div class="md-layout-item md-size-100" style="text-align: left">'
                                        +'<input type="checkbox" style="display:inline-block;vertical-align:middle;" class="md-checkbox" name="reasons_checkboxes" value="[no show]">'
                                        +'<label>No Show</label>'
                                        +'</input>'
                                        +'</div>'
                                        +'<div class="md-layout-item md-size-100" style="text-align: left">'
                                        +'<input type="checkbox" style="display:inline-block;vertical-align:middle;" class="md-checkbox" name="reasons_checkboxes" value="[abandoned]">'
                                        +'<label>Abandoned</label>'
                                        +'</input>'
                                        +'</div>'
                                        +'<div class="md-layout-item md-size-100" style="text-align: left">'
                                        +'<input type="checkbox" style="display:inline-block;vertical-align:middle;" class="md-checkbox" name="reasons_checkboxes" value="[on hold by ip]">'
                                        +'<label>On Hold by IP</label>'
                                        +'</input>'
                                        +'</div>'
                                        +'<div class="md-layout-item md-size-100" style="text-align: left">'
                                        +'<input type="checkbox" style="display:inline-block;vertical-align:middle;" class="md-checkbox" name="reasons_checkboxes" value="[on hold by agency]">'
                                        +'<label>On Hold by Agency</label>'
                                        +'</input>'
                                        +'</div>'
                                        +'<br>'
                                        +'<div class="md-layout-item md-size-100" style="text-align: left">'
                                        +'<input type="checkbox" style="display:inline-block;vertical-align:middle;" class="md-checkbox" name="reasons_checkboxes" value="[other]">'
                                        +'<label>Other</label>'
                                        +'</input>'
                                        +'</div>'
                                        +'<br>'
                                        +'<div class="md-layout-item md-size-100" style="text-align: left">'
                                        +'<label style="font-size: 20px;">Booking Notes</label>'
                                        +'<div class="md-field md-theme-default md-has-value md-has-textarea">'
                                        +  '<textarea style="border-style: solid; border-width: 1px" data-vv-name="item.other" id="cal_dialog_book_slot_note" class="md-textarea">'
                                        +  '</textarea>'
                                        +'</div>'
                                        +'</div>',
                                        showCancelButton: true,
                                        showCloseButton: true,
                                        confirmButtonClass: "md-button md-success",
                                        confirmButtonText: "Proceed",
                                        cancelButtonClass: "md-button md-danger",
                                        buttonsStyling: true,
                                        preConfirm: () => {
                                          booking_form_data_note += ' Booking Notes: ' + document.getElementById('cal_dialog_book_slot_note').value
                                          document.getElementsByName('reasons_checkboxes').forEach(element => {
                                          if (element.checked){
                                              delay_reasons.push(element.value)
                                          }                 
                                          });
                                          console.log('delay_reasons', delay_reasons) 
                                        }
                                }).then((result) => {
                                  if (result.value) {
                                    if (booking_form_data_note){
                                      booking_form_data_note += ', ' + delay_reasons.join()
                                    }else{
                                      booking_form_data_note = delay_reasons.join()
                                    }
                                    window.book_slot(this.events, selected_slot, slot_external_id, booking_form_data_note, booking_form_data_email_list, booking_form_data_additional_emails, booked_with_claimant, booked_with_instructing_party, booked_with_no_one)
                                    return
                                  }
                                })
                              }
                            })
                            // window.book_slot(this.events, selected_slot, slot_external_id, booking_form_data_note, booking_form_data_email_list, booking_form_data_additional_emails)
                          }                           
                      })
                      .catch(function(error) {
                          console.error(error.response);
                      })
                  
                }
              })
          })
          window.venueMarkers.push(marker)
        } else {
          var selected_experts = []
          var selected_postcode = ''
          var include_ranges = false
          var specific_html_content = ''
          console.log('events', events)
          const selected_supported_product = sessionStorage.getItem('selected_supported_product')
          const marker = new window.google.maps.Marker({
              position: {
                lat: events[0].longlat ? parseFloat(events[0].longlat[0]) : 0.0,
                lng: events[0].longlat ? parseFloat(events[0].longlat[1]): 0.0
              },
              title: 'Request from: [' + events[0].postcode + ']',
              map: window.venuesMap,
              icon: {
                // url: 'http://maps.google.com/mapfiles/ms/icons/red-dot.png',
                url: 'http://maps.google.com/mapfiles/ms/micons/question.png',
                scaledSize: new google.maps.Size(50, 50)
              }

              // draggable:true
            });
          marker.events = events
          marker.addListener('click', function() {
            var dialog_content = '<div class="md-field md-theme-default"><div class="md-layout md-size-100">'
            // dialog_content += '<div class="md-layout-item md-size-100">Venue: '+events[0].details.venue+'</div>'
            for (var i = 0; i < events.length; i++) {
              dialog_content += '<div class="md-layout-item md-size-100" style="border-style: solid;border-width:1px">'
                                + '<p>Appointment After: ' + moment(current_case_object.instructions.recommended_appointment_range_start).format('DD/MM/YYYY') + '</p>'
                                + '<p>Appointment Before: ' + moment(current_case_object.instructions.recommended_appointment_range_end).format('DD/MM/YYYY') + '</p>'
                                +'<input type="checkbox" style="display:inline-block;vertical-align:middle;" class="md-checkbox" id="include_ranges" value="true" checked>'
                                +'Do you want to Include the Special Instruction date range in the email?'
                                +'</input>'
                                +'</div>'
                                +'<div class="md-layout-item md-size-100" style="border-style: solid;border-width:1px">'
                                +   '<div class="md-field md-theme-default md-has-value md-has-textarea">'
                                +     '<label style="font-size: 20px;">Additional EMAIL content</label>'
                                +     '<textarea id="specific_html_content" class="md-textarea">'
                                +     '</textarea>'
                                +   '</div>'
                                +'</div>'
                                + '<br>'
                                +'<div class="md-layout-item md-size-100">' +
                                '<input type="radio" style="display:inline-block;vertical-align:middle;zoom:1.5;" class="md-radio" name="request_slot_checkboxes" value="'+events[i].details.expert_id+'">'+
                                '<span style="font-size: 25px">' + events[i].title + '</span>' +
                                '</input>' +
                                '</div>'                        
            }
            dialog_content += '</div></div>'
            selected_postcode = events[0].postcode
            Swal.fire({
              title: 'Request slots from the options below',
              html: dialog_content,
              width: '1000px',
              showCancelButton: true,
              confirmButtonColor: '#3085d6',
              cancelButtonColor: '#d33',
              confirmButtonText: 'Email selected Experts!',
              preConfirm: () => {
                selected_experts = []
                document.getElementsByName('request_slot_checkboxes').forEach(element => {
                  if(element.checked && !selected_experts.includes(Number(element.value))){
                    selected_experts.push(Number(element.value))
                  }
                });
                specific_html_content = document.getElementById('specific_html_content').value
                console.log('include_ranges.value', document.getElementById('include_ranges').value)
                if (document.getElementById('include_ranges').checked){
                  include_ranges = true
                }else{
                  include_ranges = false
                }
                console.log(selected_experts)
              }
            }).then((result) => {
              if (result.value) {
                NProgress.start();
                if (selected_experts.length > 0){
                  console.log('selected_experts ', selected_experts)
                  console.log('selected_product ', Number(selected_supported_product))
                  console.log('case_id ', Number(current_case_object.id))
                  console.log('selected_postcode ', selected_postcode)
                  console.log(selected_experts)
                  const attachments = JSON.parse(sessionStorage.getItem('appointments_selected_attachments'))
                  console.log('attachments', attachments)

                  //assuming is only 1 selection = 1 expert
                  var computed_event = null
                  for (var i in events){
                    if (events[i].details.expert_id === selected_experts[0]){
                      computed_event = events[i]
                    }
                  }

                  const slot_request_notification_document_details = expertSlotRequestPDF(computed_event, true, include_ranges)
                  var form_data = new FormData()
                  form_data.append('appointment_request_notification_document', slot_request_notification_document_details[0])
                  form_data.append('appointment_request_notification_document_name', slot_request_notification_document_details[1])
                  form_data.append('case_id', current_case_object.id)
                  window.$http
                    .create({headers: { 'Content-Type': 'application/form-data'}})
                    .post(window.url__appointment_attach_notification_pdfs, form_data)
                    .then(response =>{
                      window.$http
                      .post(window.url__email_expert_for_slot_request, {'experts': selected_experts, 
                                                                        'selected_product': Number(selected_supported_product), 
                                                                        'case_id': Number(current_case_object.id), 
                                                                        'selected_postcode': selected_postcode,
                                                                        'attachments': attachments,
                                                                        'include_ranges': include_ranges,
                                                                        'specific_html_content': specific_html_content,
                                                                        'appointment_request_notification_document': response.data.appointment_request_notification_document_id
                                                                        })
                      .then(response => {
                        NProgress.done();
                        Swal.fire('Good job!', 'The experts have been notified!', 'success')
                      })
                      .catch(function(error) {
                        NProgress.done();
                        Swal.fire("Error", "The slot could not be updated.</br> "+error.response.statusText, "error")
                      });
                    })  
                }else{
                  NProgress.done();
                  Swal.fire('Error', 'Nothing Selected!', 'error')
                }
              }
            })
          })
          window.venueMarkers.push(marker)
        }

        
      })
    if (sessionStorage.getItem('current_case_object')){
      const current_case_object = JSON.parse(sessionStorage.getItem('current_case_object'))
      if(current_case_object.longlat){
          const currentCaseMarker = new window.google.maps.Marker({
            position: {
              lat: parseFloat(current_case_object.longlat[0]),
              lng: parseFloat(current_case_object.longlat[1])
            },
            title: current_case_object.label,
            map: window.venuesMap,
            // icon: 'https://maps.google.com/mapfiles/kml/paddle/blu-blank.png'
            icon:{
              url: 'http://maps.google.com/mapfiles/ms/micons/man.png',
              scaledSize: new google.maps.Size(30, 30)
            }
          });

          window.venueMarkers.push(currentCaseMarker)

          window.venuesMap.setCenter({
            lat: parseFloat(current_case_object.longlat[0]),
            lng: parseFloat(current_case_object.longlat[1])
          });

          if (window.slaRadius)
            delete window.slaRadius

          // var radius = 16093
          var radius = 16093/10 * 10
          if (window.sla_radius){
            radius = (16093/10) * window.sla_radius
          }

          var slaRadius = new google.maps.Circle({
            map: window.venuesMap,
            radius: radius,    // 10 miles in metres
            fillColor: '#AA0000',
            // draggable:true
          });
          slaRadius.bindTo('center', currentCaseMarker, 'position');

          window.venuesMap.setCenter({
            lat: parseFloat(current_case_object.longlat[0]),
            lng: parseFloat(current_case_object.longlat[1])
          });
          window.venueMarkers.push(slaRadius)
          window.slaRadius = slaRadius

      }
    }

    var uniqueMarkers = new Map();
    var isCenterSet = false;

    console.log(
      "Total number of markes to be created:" + uniqueMarkers.size
    );
    NProgress.done()
  }

export default {
  components: {
    NavTabsCard,
    AppointmentsList,
    // ReservedSlots,
    SlotSeriesGenerator,
    AppointmentRequestMultiSelectFilter,
    DatePicker
  },
  data() {
    return {
      sliders: [
        {id:1, value: 1},
      ],
      adhocAppointment: {
        selected_third_party: '-',
        datetime: null,
        venue: null,
        notes: null,
      },
      easyslot_slots_counter: 0,
      internal_slots_counter: 0,
      third_party_companies: [],
      show_third_party_booking: false,
      show_normal_booking: false,
      selected_attachments: [],
      experts_with_supported_products: null,
      selected_supported_product: [],
      selected_product: null,
      product_types: [],
      selected_specialisations: [],
      selected_experts: [],
      specialisations: {},
      supported_products: {},
      what_to_show: 'slots',
      venue_parking: null,
      venue_disable_access: null,
      venue_lift_access: null,
      venue_child_friendly: null,
      selectedDate: moment(new Date()).format('YYYY-MM-DD'),
      selectedExpert: sessionStorage.getItem("appointments_calendar_selectedExpert"),
      selectedVenue: sessionStorage.getItem("appointments_calendar_selectedVenue"),
      showAppointments: JSON.parse(sessionStorage.getItem("appointments_calendar_showAppointments")),
      experts: [],
      allExperts: [],
      venues: [],
      allVenues: [],
      calendar: null,
      current_start_date: moment(new Date()).format("DD/MM/YYYY"),
      current_end_date: moment(new Date()).add('month', 1).startOf('month').format("DD/MM/YYYY"),
      sla_radius: sessionStorage.getItem('map_radius'),
      disable_backward_button: true,
      // events: {
      //   url: this.url__calendar_events,
      //   cache: false,
      //   headers: {
      //     Authorization: "JWT " + sessionStorage.getItem("jwt")
      //   },
      //   data: function() {
      //       return {
      //           expert: sessionStorage.getItem("appointments_calendar_selectedExperts"),
      //           venue: sessionStorage.getItem("appointments_calendar_selectedVenue"),
      //           appointments: JSON.parse(sessionStorage.getItem("appointments_calendar_showAppointments")) ? 1 : 0,
      //           selected_supported_product: sessionStorage.getItem("selected_supported_product"),
      //           venue_parking: sessionStorage.getItem("appointments_calendar_venue_parking"),
      //           venue_disable_access: sessionStorage.getItem("appointments_calendar_venue_disable_access"),
      //           venue_lift_access: sessionStorage.getItem("appointments_calendar_venue_lift_access"),
      //           venue_child_friendly: sessionStorage.getItem("appointments_calendar_venue_child_friendly"),
      //       }
      //   },
      // },
    };
  },
  created() {
    //reset calendar local storage values
    sessionStorage.removeItem("appointments_calendar_selectedExperts"),
    sessionStorage.removeItem("appointments_calendar_selectedVenue"),
    sessionStorage.removeItem("appointments_selected_attachments"),
    // sessionStorage.setItem("appointments_selectedDate", new Date().toISOString()),
    sessionStorage.removeItem("appointments_calendar_venue_parking", false),
    sessionStorage.removeItem("appointments_calendar_venue_disable_access", false),
    sessionStorage.removeItem("appointments_calendar_venue_lift_access", false),
    sessionStorage.removeItem("appointments_calendar_venue_child_friendly", false),
    sessionStorage.setItem('map_radius', 10)
    this.sla_radius = 10
    // this.$http
    //   .get(this.url__expert_quick_search_compact)
    //   .then(response => {
    //     this.allExperts = response.data;
    //   })
    //   .catch(function(error) {
    //     console.error(error.response);
    //   });
    // this.$http
    //   .get(this.url__venue_quick_search_compact)
    //   .then(response => {
    //     this.allVenues = response.data;
    //   })
    //   .catch(function(error) {
    //     console.error(error.response);
    //   });
    
    // this.$http
    //   .get(this.url__experts_with_specialisations)
    //   .then(response => {
    //     this.experts_with_specialisations = response.data;
    //   })
    //   .catch(function(error) {
    //     console.error(error.response);
    //   });

    window.$http = this.$http
    window.url__appointmentslot = this.url__appointmentslot
    window.url__calendar_appointmentslot = this.url__calendar_appointmentslot
    window.url__appointment_attach_claimant_notification_claimant_pdf = this.url__appointment_attach_claimant_notification_claimant_pdf
    window.expertSlotRequestPDF = this.expertSlotRequestPDF
    window.url__appointment_attach_notification_pdfs = this.url__appointment_attach_notification_pdfs
    window.url__calendar_book_slot = this.url__calendar_book_slot
    window.url__notifications_email_expert_apointment_confirmation = this.url__notifications_email_expert_apointment_confirmation
    window.url__email_expert_for_slot_request = this.url__email_expert_for_slot_request
    window.url__calendar_events = this.url__calendar_events
    window.url__appointment_exceeding_sla = this.url__appointment_exceeding_sla
    window.url__appointment_reserve_slot = this.url__appointment_reserve_slot
    window.book_slot = this.book_slot
    window.url__case_details = this.url__case_details
    window.refreshCase = this.refreshCase
    window.increment_internal_slots_counter = this.increment_internal_slots_counter
    window.increment_easyslot_slots_counter = this.increment_easyslot_slots_counter
    window.reset_slots_counters = this.reset_slots_counters
    if(!this.selectedExpert){
      this.setCurrentExpert(sessionStorage.getItem("appointments_calendar_selectedExpert"))
    }
    if(!this.selectedVenue){
      this.setCurrentExpert(sessionStorage.getItem("appointments_calendar_selectedVenue"))
    }
    // this.refreshCurrentCase()
    if (sessionStorage.getItem("current_case_object")){
      const current_case_object = JSON.parse(sessionStorage.getItem("current_case_object"))
      if (!current_case_object.claimant.postcode){
        Swal.fire({
          width: '1000px',
          type: 'warning',
          title: "Claimant's Postcode is not populated",
          html: "<b>Please populate Claimant's Postcode before proceeding!</b>",
          showConfirmButton: false,
          showCancelButton: false,
        })
      }
      this.venue_parking = this.currentCase.instructions.venue_parking
      this.venue_disable_access = this.currentCase.instructions.venue_disable_access
      this.venue_lift_access = this.currentCase.instructions.venue_lift_access
      this.venue_child_friendly = this.currentCase.instructions.venue_child_friendly
    }else{
      Swal.fire({
        width: '1000px',
        type: 'warning',
        title: 'Case has not been selected!',
        html: '<b>Please select a Case before proceeding!</b>',
        showConfirmButton: false,
        showCancelButton: false,
      })
    }
    this.selected_supported_product = '-'
    
  },
  methods: {
    ...mapActions([
      'setCurrentCase',
      'setCurrentCaseLabel',
      'setCurrentExpert',
      'setCurrentVenue',
      'refreshCurrentCase'
    ]),
    increment_internal_slots_counter(){
      this.internal_slots_counter += 1
    },
    increment_easyslot_slots_counter(){
      this.easyslot_slots_counter += 1
    },
    reset_slots_counters(){
      this.internal_slots_counter = 0
      this.easyslot_slots_counter = 0
    },
    retrieveData(){
      console.log('retrieving data!')
      $("#fullCalendar").fullCalendar('removeEvents')
      NProgress.start()
      $("#fullCalendar").fullCalendar("refetchEvents")
    },
    requestSlotThirdParty(id){
      if (id === '-'){
        Swal.fire(
          'Select a Company',
          'Please select a Third Party Company!',
          'warning'
        )
        return
      }
      Swal.fire({
      title: 'Are you sure?',
      text: "Do you want to request an Appointment Slot?",
      type: 'warning',
      showCancelButton: true,
      confirmButtonColor: '#3085d6',
      cancelButtonColor: '#d33',
      confirmButtonText: 'Yes!'
      }).then((result) => {
        if (result.value) {
          const current_case_object = JSON.parse(sessionStorage.getItem('current_case_object'))
          const attachments = JSON.parse(sessionStorage.getItem('appointments_selected_attachments'))
          console.log(id)
          this.$http
            .post(this.url__email_third_party_company_for_slot_request, {'company_id': id, 
                                                                        'selected_product': this.selected_supported_product, 
                                                                        'case_id': Number(current_case_object.id), 
                                                                        'attachments': attachments,
                                                                        'include_ranges': false,
                                                                        'specific_html_content': '',
                                                                        'venue': this.adhocAppointment.venue
                                                                        })
            .then(response => {
              Swal.fire('Good job!', 'The Third Party Company has been notified!', 'success')
            })
            .catch(function(error) {
              Swal.fire("Error", "The Third Party Company could not be notified.</br> "+error.response.statusText, "error")
            });
        }
      })
    },
    bookAdhocAppointment(){
      const current_case_object = JSON.parse(sessionStorage.getItem('current_case_object'))
      console.log('company_id', this.adhocAppointment.selected_third_party)
      console.log('venue', this.adhocAppointment.venue)
      console.log('notes', this.adhocAppointment.notes)
      console.log('datetime', this.adhocAppointment.datetime)
      console.log('selected_product', this.selected_supported_product)
      var form_data = new FormData()
      var email_list = []
      var additional_emails = ''
      var appointment_type = ''
      for (var index in this.product_types){
        if (this.product_types[index].id === this.selected_supported_product){
          console.log('matching product: ', this.product_types[index])
          if (this.product_types[index].name.includes('Nerve Conduction Test')){
            appointment_type = 'Nerve Conduction Test'
          }else if(this.product_types[index].name.includes('Audiology')){
            appointment_type = 'Audiology'
          }else if(this.product_types[index].name.includes('X-Ray')){
            appointment_type = 'X-Ray'
          }else if(this.product_types[index].name.includes('Ultrasound')){
            appointment_type = 'Ultrasound'
          }else if(this.product_types[index].name.includes('MRI')){
            appointment_type = 'MRI'
          }else if(this.product_types[index].name.includes('Councelling')){
            appointment_type = 'Councelling'
          }else if(this.product_types[index].name.includes('CBT')){
            appointment_type = 'CBT'
          }else if(this.product_types[index].name.includes('Osteopathy')){
            appointment_type = 'Osteopathy'
          }else if(this.product_types[index].name.includes('Physiotherapy')){
            appointment_type = 'Physiotherapy'
          }
          break
        }
      }
      var data = {'venue': this.adhocAppointment.venue,
                  'appointment_type': appointment_type,
                  'appointment_datetime': this.adhocAppointment.datetime}
      // form_data.append('venue', this.adhocAppointment.venue)
      // form_data.append('appointment_type', appointment_type)
      // form_data.append('appointment_datetime', this.adhocAppointment.datetime)
      var claimant_notification_document_details = claimantAppointmentNotificationPDF(data, true, true)

      form_data.append('claimant_notification_document', claimant_notification_document_details[0])
      form_data.append('claimant_notification_document_name', claimant_notification_document_details[1])
      this.$http
        .create({headers: { 'Content-Type': 'application/form-data'}})
        .post(this.url__appointment_attach_claimant_notification_claimant_pdf, form_data)
        .then(response =>{
          Swal.fire({
            width: '1000px',
            title: 'Notification Emails',
            html: '<div class="md-layout-item md-size-100" style="text-align:left">'
                  +'<input type="checkbox" style="display:inline-block;vertical-align:middle;" class="md-checkbox" name="who_to_email_checkboxes" value="email_claimant" checked>'
                  +'<label>Email Claimant: ' + current_case_object.claimant.email + '</label>'
                  +'</input>'
                  +'</div>'
                  +'<div class="md-layout-item md-size-100" style="text-align:left">'
                  +'<input type="checkbox" style="display:inline-block;vertical-align:middle;" class="md-checkbox" name="who_to_email_checkboxes" value="email_instructing_party" checked>'
                  +'<label>Email Instructing Party File Handler: ' + current_case_object.instructing_party.file_handler_email + '</label>'
                  +'</input>'
                  +'</div>'
                  +'<div class="md-layout-item md-size-100">'
                  +   '<div class="md-field md-theme-default md-has-value md-has-textarea">'
                  +     '<label>Additional emails seperated by a ,</label>'
                  +     '<textarea data-vv-name="item.other" id="cal_dialog_book_slot_additional_emails" class="md-textarea">'
                  +     '</textarea>'
                  +   '</div>'
                  +'</div>',
              showCancelButton: true,
              confirmButtonClass: "md-button md-success",
              confirmButtonText: "Book it",
              cancelButtonClass: "md-button md-danger",
              buttonsStyling: true,
              preConfirm: () => {
                additional_emails = document.getElementById('cal_dialog_book_slot_additional_emails').value
                document.getElementsByName('who_to_email_checkboxes').forEach(element => {
                  if(element.checked){
                    email_list.push(element.value)
                  }
                });
              }
              }).then((result) => {
              if (result.value) {
                this.$http
                  .post(this.url__adhoc_book_slot, {company_id: this.adhocAppointment.selected_third_party,
                                                    venue: this.adhocAppointment.venue,
                                                    notes: this.adhocAppointment.notes,
                                                    datetime: this.adhocAppointment.datetime,
                                                    selected_product: this.selected_supported_product,
                                                    case_id: current_case_object.id,
                                                    claimant_notification_document: response.data.document_id,
                                                    email_list: email_list,
                                                    additional_emails: additional_emails})
                  .then(response => {
                    var booking_msg = ''
                    if (response.data.email_instructing_party === 1) {
                      booking_msg += '</br> <span style="color: green">Email notification sent to Instructing party.</span> '
                    }else{
                      booking_msg += '</br> <span style="color: red">Email notification NOT sent to Instructing party.</span> '
                    }
                    if (response.data.email_claimant === 1) {
                      booking_msg += '</br> <span style="color: green">Email notification sent to Claimant.</span> '
                    }else{
                      booking_msg += '</br> <span style="color: red">Email notification NOT sent to Claimant.</span> '
                    }
                    if (response.data.additional_emails === 1) {
                      booking_msg += '</br> <span style="color: green">Email notification sent to Additional Emails.</span> '
                    }else{
                      booking_msg += '</br> <span style="color: red">Email notification NOT sent to Additional Emails.</span> '
                    }
                    if (response.data.sms_claimant === 1) {
                      booking_msg += '</br> <span style="color: green">SMS notification sent to Claimant.</span> '
                    }else{
                      booking_msg += '</br> <span style="color: red">SMS notification NOT sent to Claimant.</span> '
                    }
                    Swal.fire({
                      title: 'Good job!',
                      html: 'Adhoc Appointment Booked!' + booking_msg,
                      type: 'success'
                    })
                    this.selected_supported_product = '-'
                    this.show_normal_booking = false
                    this.show_third_party_booking = false
                    this.adhocAppointment.venue = null
                    this.adhocAppointment.datetime = null
                    this.adhocAppointment.selected_third_party = '-'
                    this.adhocAppointment.notes = null
                    claimantAppointmentNotificationPDF(data, false, true)

                  })
                  .catch(function(error) {
                      console.error(error.response);
                      Swal.fire(
                        'Oops..',
                        'Appointment could not be booked!',
                        'error'
                      )
                  })
              }
            })
        })
        .catch(function(error) {
            console.error(error.response);
            Swal.fire(
              'Oops..',
              'Appointment could not be booked!',
              'error'
            )
        })
    },
    refreshCase(){
      const current_case_object = JSON.parse(sessionStorage.getItem('current_case_object'))
      if (current_case_object.id){
        window.$http
          .get(window.url__case_details + current_case_object.id + '/')
          .then(response => {
            sessionStorage.setItem('current_case_object', JSON.stringify(response.data))                  
          })
          .catch(function(error) {
              console.error(error.response);
              Swal.fire(
                'Oops..',
                'Case could not be refreshed!',
                'error'
              )
          })
      }
    },
    backAmonth(){
      NProgress.start();
      console.log('3')
      var calendar = $("#fullCalendar")
      calendar.fullCalendar('prev')
      if (moment(calendar.fullCalendar('getDate')).month() === moment(new Date()).month()){
        this.current_start_date = moment(new Date()).format("DD/MM/YYYY");
        this.disable_backward_button = true
      }else{
        this.current_start_date = calendar.fullCalendar('getDate').format("DD/MM/YYYY");
        this.disable_backward_button = false
      }
      this.current_end_date = calendar.fullCalendar('getDate').add('month', 1).startOf('month').format("DD/MM/YYYY")
      cleanupMarkers()
    },
    forwardAmonth(){
      // current_start_date: moment(new Date()).startOf('month').format("DD/MM/YYYY"),
      // current_end_date: moment(new Date()).subtract('month', 1).endOf('month').add('month', 12).format("DD/MM/YYYY"),
      NProgress.start();
      console.log('4')
      var calendar = $("#fullCalendar")
      calendar.fullCalendar('next')
      if (moment(calendar.fullCalendar('getDate')).month() === moment(new Date()).month()){
        this.current_start_date = moment(new Date()).format("DD/MM/YYYY");
        this.disable_backward_button = true
      }else{
        this.current_start_date = calendar.fullCalendar('getDate').format("DD/MM/YYYY");
        this.disable_backward_button = false
      }
      this.current_end_date = calendar.fullCalendar('getDate').add('month', 1).startOf('month').format("DD/MM/YYYY")
      cleanupMarkers()
    },
    caseSelected() {
      console.log('Case selected..')
    },
    book_slot(events, selected_slot, slot_external_id, booking_form_data_note, booking_form_data_email_list, booking_form_data_additional_emails, booked_with_claimant=false, booked_with_instructing_party=false, booked_with_no_one=false){
      // booking_form_data_note, 'email_list': booking_form_data_email_list, 'additional_emails': booking_form_data_additional_emails, 'report_type': selected_supported_product, 'attachments': attachments 
      const selected_supported_product = sessionStorage.getItem('selected_supported_product')
      const current_case_object = JSON.parse(sessionStorage.getItem('current_case_object'))
      const attachments = JSON.parse(sessionStorage.getItem('appointments_selected_attachments'))
      if(slot_external_id){
        var external_link = "https://easyslot.co.uk/Home/ManageAppointmentSlot?AppId=" + slot_external_id
        console.log(selected_slot)
        console.log(slot_external_id)
        Swal.mixin({
          width: `1200px`,
          confirmButtonText: 'Next &rarr;',
          showCancelButton: true,
          progressSteps: ['1', '2']
        }).queue([
          {
          title: "Easyslot Login",                 
          html: '<h1 style="color: red">Open a new window and Login to Easyslot</h1>',
          showCancelButton: true,
          confirmButtonClass: "md-button md-success",
          confirmButtonText: "Proceed to Booking Form",
          cancelButtonClass: "md-button md-danger",
          buttonsStyling: true,
          },
          {
            title: "Easyslot details and link to booking form",
            html: '<div class="md-layout-item md-size-100">'
                  + `<a style="font-size: 35px" href=${external_link} target="_blank">Click on this link to go to the Easyslot booking form</a>`
                  + "</div>"
                  + "<br>"
                  +'<div class="md-layout-item md-size-100" style="text-align: left">'
                  +"<label>Claimant's Title: </label>" + '<input type="text" style="font-weight: bold;" value="' + current_case_object.claimant.title + '" disabled>'
                  +"</div>"
                  +"<br>"
                  +'<div class="md-layout-item md-size-100" style="text-align: left">'
                  +"<label>Claimant's Forename: </label>" + '<input type="text" style="font-weight: bold;" value="' + current_case_object.claimant.first_name + '" disabled>'
                  +"</div>"
                  +"<br>"
                  +'<div class="md-layout-item md-size-100" style="text-align: left">'
                  +"<label>Claimant's Surname: </label>" + '<input type="text" style="font-weight: bold;" value="' + current_case_object.claimant.last_name + '" disabled>'
                  +"</div>"
                  +"<br>"
                  +'<div class="md-layout-item md-size-100" style="text-align: left">'
                  +"<label>Claimant's Gender: </label>" + '<input type="text" style="font-weight: bold;" value="' + current_case_object.claimant.gender + '" disabled>'
                  +"</div>"
                  +"<br>"
                  +'<div class="md-layout-item md-size-100" style="text-align: left">'
                  +"<label>Claimant's Date of Birth: </label>" + '<input type="text" style="font-weight: bold;" value="' + moment(current_case_object.claimant.date_of_birth).format('DD/MM/YYYY') + '" disabled>'
                  +"</div>"
                  +"<br>"
                  +'<div class="md-layout-item md-size-100" style="text-align: left">'
                  +"<label>Claimant's Home Tel: </label>" + '<input type="text" style="font-weight: bold;" value="' + current_case_object.claimant.telephone1 + '" disabled>'
                  +"</div>"
                  +"<br>"
                  +'<div class="md-layout-item md-size-100" style="text-align: left">'
                  +"<label>Claimant's Work Tel: </label>" + '<input type="text" style="font-weight: bold;" value="' + current_case_object.claimant.telephone2 + '" disabled>'
                  +"</div>"
                  +"<br>"
                  +'<div class="md-layout-item md-size-100" style="text-align: left">'
                  +"<label>Claimant's Mobile: </label>" + '<input type="text" style="font-weight: bold;" value="' + current_case_object.claimant.mobile1 + '" disabled>'
                  +"</div>"
                  +"<br>"
                  +'<div class="md-layout-item md-size-100" style="text-align: left">'
                  +"<label>Claimant's Email: </label>" + '<input type="text" style="font-weight: bold;" value="' + current_case_object.claimant.email + '" disabled>'
                  +"</div>"
                  +"<br>"
                  +'<div class="md-layout-item md-size-100" style="text-align: left">'
                  +"<label>Claimant's Postcode: </label>" + '<input type="text" style="font-weight: bold;" value="' + current_case_object.claimant.postcode + '" disabled>'
                  +"</div>"
                  +"<br>"
                  +'<div class="md-layout-item md-size-100" style="text-align: left">'
                  +"<label>Claimant's Address Line 1: </label>" + '<input type="text" style="font-weight: bold;" value="' + current_case_object.claimant.address1 + '" disabled>'
                  +"</div>"
                  +"<br>"
                  +'<div class="md-layout-item md-size-100" style="text-align: left">'
                  +"<label>Claimant's Address Line 2: </label>" + '<input type="text" style="font-weight: bold;" value="' + current_case_object.claimant.address2 + '" disabled>'
                  +"</div>"
                  +"<br>"
                  +'<div class="md-layout-item md-size-100" style="text-align: left">'
                  +"<label>Claimant's Address Town/City: </label>" + '<input type="text" style="font-weight: bold;" value="' + current_case_object.claimant.address3 + '" disabled>'
                  +"</div>"
                  +"<br>"
                  +'<div class="md-layout-item md-size-100" style="text-align: left">'
                  +"<label>Claimant's Accident Date: </label>" + '<input type="text" style="font-weight: bold;" value="' + moment(current_case_object.accident.date).format('DD/MM/YYYY') + '" disabled>'
                  +"</div>"
                  +"<br>"
                  +'<div class="md-layout-item md-size-100" style="text-align: left">'
                  +"<label>Claimant's Accident Type: </label>" + '<input type="text" style="font-weight: bold;" value="' + current_case_object.accident.type + '" disabled>'
                  +"</div>"
                  +"<br>"
                  +'<div class="md-layout-item md-size-100" style="text-align: left">'
                  +"<label>Claimant's Agency Ref: </label>" + '<input type="text" style="font-weight: bold;" value="' + current_case_object.claimant.last_name.substring(0,3) + current_case_object.id + '" disabled>'
                  +"</div>"
                  +"<br>"
                  +'<div class="md-layout-item md-size-100" style="text-align: left">'
                  +"<label>Claimant's Solicitor: </label>" + '<input type="text" style="font-weight: bold;" value="' + current_case_object.instructing_party.name + '" disabled>'                            +"</div>"
                  +"</div>"
                  +"<br>"
                  +'<div class="md-layout-item md-size-100" style="text-align: left">'
                  +"<label>Claimant's Solicitor Ref: </label>" + '<input type="text" style="font-weight: bold;" value="' + current_case_object.instructing_party.instruction_party_reference + '" disabled>'
                  +"</div>"
                  +"<br>"
                  +'<div class="md-layout-item md-size-100" style="text-align: left">'
                  +"<label>MedCo ID: </label>" + '<input type="text" style="font-weight: bold;" value="' + current_case_object.instructing_party.medco_id + '" disabled>'
                  +"</div>",
                  
            showCancelButton: true,
            confirmButtonClass: "md-button md-success",
            confirmButtonText: "Successfully Booked on Easyslot",
            cancelButtonClass: "md-button md-danger",
            buttonsStyling: true,
          },
        ]).then((result) => {
          if (result.value){
            NProgress.start()
            var event = null
            for (var index in events){
              if (Number(events[index].id) === Number(selected_slot)){
                event = events[index]
              }
            }
            const claimant_notification_document_details = claimantAppointmentNotificationPDF(event, true)
            const expert_notification_document_details = expertAppointmentNotificationPDF(event, true)
            var form_data = new FormData()
            form_data.append('claimant_notification_document', claimant_notification_document_details[0])
            form_data.append('claimant_notification_document_name', claimant_notification_document_details[1])
            form_data.append('expert_notification_document', expert_notification_document_details[0])
            form_data.append('expert_notification_document_name', expert_notification_document_details[1])
            form_data.append('case_id', current_case_object.id)
            window.$http
              .create({headers: { 'Content-Type': 'application/form-data'}})
              .post(window.url__appointment_attach_notification_pdfs, form_data)
              .then(response =>{
                window.$http
                  .create({headers: { 'Content-Type': 'application/json'}})
                  .put(window.url__calendar_book_slot, {'slot': selected_slot, 
                                                        'case': current_case_object.id, 
                                                        'note': booking_form_data_note, 
                                                        'email_list': booking_form_data_email_list, 
                                                        'additional_emails': booking_form_data_additional_emails, 
                                                        'report_type': selected_supported_product, 
                                                        'attachments': attachments,
                                                        'claimant_notification_document' : response.data.claimant_document_id,
                                                        'expert_notification_document' : response.data.expert_document_id,
                                                        'booked_with_claimant': booked_with_claimant,
                                                        'booked_with_instructing_party': booked_with_instructing_party,
                                                        'booked_with_no_contact': booked_with_no_one
                                                        })
                  .then(response => {
                    var booking_msg = 'Slot booked!'
                    if (response.data.email_expert === 1) {
                      booking_msg += '</br> <span style="color: green">Email notification sent to Expert.</span> '
                    }else{
                      booking_msg += '</br> <span style="color: red">Email notification NOT sent to Expert.</span> '
                    }
                    if (response.data.email_instructing_party === 1) {
                      booking_msg += '</br> <span style="color: green">Email notification sent to Instructing party.</span> '
                    }else{
                      booking_msg += '</br> <span style="color: red">Email notification NOT sent to Instructing party.</span> '
                    }
                    if (response.data.email_claimant === 1) {
                      booking_msg += '</br> <span style="color: green">Email notification sent to Claimant.</span> '
                    }else{
                      booking_msg += '</br> <span style="color: red">Email notification NOT sent to Claimant.</span> '
                    }
                    if (response.data.sms_claimant === 1) {
                      booking_msg += '</br> <span style="color: green">SMS notification sent to Claimant.</span> '
                    }else{
                      booking_msg += '</br> <span style="color: red">SMS notification NOT sent to Claimant.</span> '
                    }
                    
                    if ( response.data.invoice ) {
                      booking_msg += '<li><a href="/invoice/edit/'+response.data.invoice+'">Proforma invoice: '+response.data.invoice+'</a></li>'
                    }
                    booking_msg += '</ul></div>'

                    if (response.data.medical_report) {
                      booking_msg += '</br> Dummy ' + response.data.medical_report + ' created. '
                    }
                    Swal.fire("Good job!", booking_msg, "success")
                    //As clients asked, claimant appointment notificiation .PDF file is downloaded 
                    //to remind them to send it to the claimant
                    claimantAppointmentNotificationPDF(event, false)
                    //refreshing the case to make sure new appointment is reflected
                    window.refreshCase()
                    console.log('Case refreshed')
                    $("#fullCalendar").fullCalendar("refetchEvents")
                    NProgress.done()
                    })
                  .catch(function(r) {
                    NProgress.done()
                    console.log(typeof(r), r)
                    if( 401 == r.request.status ){
                      window.location.href = '/'
                    }
                    if(r.response && r.response.data){
                        var error_message = ''
                        for (var prop in r.response.data) {
                          error_message += '</br>'+prop+': '+r.response.data[prop]
                        }
                        Swal.fire("Error", "The slot could not be updated.</br> "+error_message, "error")
                    } else {
                      Swal.fire("Error", "The slot could not be updated.</br> "+r.response, "error")
                    }
                  });
              })
          }
        })
      }else{
        NProgress.start()
        var event = null
        for (var index in events){
          if (Number(events[index].id) === Number(selected_slot)){
            event = events[index]
          }
        }
        const claimant_notification_document_details = claimantAppointmentNotificationPDF(event, true)
        const expert_notification_document_details = expertAppointmentNotificationPDF(event, true)
        var form_data = new FormData()
        form_data.append('claimant_notification_document', claimant_notification_document_details[0])
        form_data.append('claimant_notification_document_name', claimant_notification_document_details[1])
        form_data.append('expert_notification_document', expert_notification_document_details[0])
        form_data.append('expert_notification_document_name', expert_notification_document_details[1])
        form_data.append('case_id', current_case_object.id)
        window.$http
          .create({headers: { 'Content-Type': 'application/form-data'}})
          .post(window.url__appointment_attach_notification_pdfs, form_data)
          .then(response =>{
            window.$http
              .create({headers: { 'Content-Type': 'application/json'}})
              .put(window.url__calendar_book_slot, {'slot': selected_slot, 
                                                    'case': current_case_object.id, 
                                                    'note': booking_form_data_note, 
                                                    'email_list': booking_form_data_email_list, 
                                                    'additional_emails': booking_form_data_additional_emails, 
                                                    'report_type': selected_supported_product, 
                                                    'attachments': attachments,
                                                    'claimant_notification_document' : response.data.claimant_document_id,
                                                    'expert_notification_document' : response.data.expert_document_id,
                                                    'booked_with_claimant': booked_with_claimant,
                                                    'booked_with_instructing_party': booked_with_instructing_party,
                                                    'booked_with_no_contact': booked_with_no_one
                                                    })
              .then(response => {
                var booking_msg = 'Slot booked!'
                if (response.data.email_expert === 1) {
                  booking_msg += '</br> <span style="color: green">Email notification sent to Expert.</span> '
                }else{
                  booking_msg += '</br> <span style="color: red">Email notification NOT sent to Expert.</span> '
                }
                if (response.data.email_instructing_party === 1) {
                  booking_msg += '</br> <span style="color: green">Email notification sent to Instructing party.</span> '
                }else{
                  booking_msg += '</br> <span style="color: red">Email notification NOT sent to Instructing party.</span> '
                }
                if (response.data.email_claimant === 1) {
                  booking_msg += '</br> <span style="color: green">Email notification sent to Claimant.</span> '
                }else{
                  booking_msg += '</br> <span style="color: red">Email notification NOT sent to Claimant.</span> '
                }
                if (response.data.sms_claimant === 1) {
                  booking_msg += '</br> <span style="color: green">SMS notification sent to Claimant.</span> '
                }else{
                  booking_msg += '</br> <span style="color: red">SMS notification NOT sent to Claimant.</span> '
                }
                
                if ( response.data.invoice ) {
                  booking_msg += '<li><a href="/invoice/edit/'+response.data.invoice+'">Proforma invoice: '+response.data.invoice+'</a></li>'
                }
                booking_msg += '</ul></div>'

                if (response.data.medical_report) {
                  booking_msg += '</br> Dummy ' + response.data.medical_report + ' created. '
                }
                Swal.fire("Good job!", booking_msg, "success")
                //As clients asked, claimant appointment notificiation .PDF file is downloaded 
                //to remind them to send it to the claimant
                claimantAppointmentNotificationPDF(event, false)
                //refreshing the case to make sure new appointment is reflected
                window.refreshCase()
                console.log('Case refreshed')
                $("#fullCalendar").fullCalendar("refetchEvents")
                NProgress.done()
                })
              .catch(function(r) {
                NProgress.done()
                console.log(typeof(r), r)
                // if 401 => route to login page..
                if( 401 == r.request.status ){
                  window.location.href = '/'
                }
                if(r.response && r.response.data){
                    var error_message = ''
                    for (var prop in r.response.data) {
                      error_message += '</br>'+prop+': '+r.response.data[prop]
                    }
                    Swal.fire("Error", "The slot could not be updated.</br> "+error_message, "error")
                } else {
                  Swal.fire("Error", "The slot could not be updated.</br> "+r.response, "error")
                }
              });
          })
        
      }
    },
    getExperts(term) {
      console.log('getExperts', term)

      const searchTerm = term
      this.experts = new Promise(resolve => {
        if (!searchTerm) {
          resolve(this.allExperts.map(x => x.label));
        } else {
          const lcTerm = searchTerm.toLowerCase();
          this.experts = this.allExperts.filter(({ label }) => {
            return label.toLowerCase().includes(lcTerm);
           }).map(x => x.label);
          resolve(this.experts);
        }
      });
    },
    getVenues(term) {
      const searchTerm = term
      this.venues = new Promise(resolve => {
        if (!searchTerm) {
          resolve(this.allVenues.map(x => x.label));
        } else {
          const lcTerm = searchTerm.toLowerCase();
          this.venues = this.allVenues.filter(({ label }) => {
            return label.toLowerCase().includes(lcTerm);
           }).map(x => x.label);
          resolve(this.venues);
        }
      });
    },
    printReport() {
      var events = $("#fullCalendar").fullCalendar("clientEvents")

      var eventsToExpert = new Map()
      for (var i = 0; i < events.length; i++) {
        if(!eventsToExpert.has(events[i].details.expert)){
          eventsToExpert.set(events[i].details.expert, [])
        }
        eventsToExpert.get(events[i].details.expert).push(events[i])
      }

      var columns = ["", "Time", "Ref", "Claimant", "Acc. Date", "Cl. Tel", "Agency", "Instructing Party", "Special Instructions"]
      var doc = new jsPDF('l', 'pt')

      var rows = []
      var markersMap = new Map()
      var markerId = 0

      eventsToExpert.forEach((events, expert, _m_) => {
        events.sort(function (a, b) {
          return a.start.valueOf() - b.start.valueOf();
        })
        var current_venue = null
        var current_date = null
        for (var i = 0; i < events.length; i++) {
          if (events[i].details.venue != current_venue || events[i].start.format('DD/MM/YYYY') != current_date){
            // Switching the venue - we need to insert special row with the venue name at this point
            current_venue = events[i].details.venue
            current_date = events[i].start.format('DD/MM/YYYY')
            rows.push(['-', markerId])
            markersMap.set(markerId, expert+' at '+events[i].details.venue+' on '+events[i].start.format('DD/MM/YYYY'))
            markerId += 1
          }
          if(events[i].appointment){
            rows.push([ i+1,
            events[i].start.format('hh:mm'),
            events[i].appointment.reference || '',
            events[i].appointment.claimant || '',
            (events[i].appointment.accident_date && events[i].appointment.accident_date.format) ? events[i].appointment.accident_date.format('DD/MM/YYYY') :  events[i].appointment.accident_date,
            events[i].appointment.claimant_tel || '',
            events[i].appointment.agency || '',
            events[i].appointment.instructing_party || '',
            events[i].appointment.special_instructions || ''])
          } else {
            rows.push([ i+1,
                      events[i].start.format('hh:mm'),
                      '',
                      '',
                      '',
                      '',
                      '',
                      '',
                      ''])
          }
        }
      })

      doc.autoTable(columns, rows, {
        theme: 'grid',
        startY: 20, //doc.autoTable.previous.finalY + 15,
        margin: { horizontal: 10 },
        bodyStyles: { valign: 'top' },
        columnStyles: {
          0: {columnWidth: 25},
          1: {columnWidth: 40},
          2: {columnWidth: 55},
          3: {columnWidth: 100, overflow: 'linebreak'},
          4: {columnWidth: 60, overflow: 'linebreak'},
          5: {columnWidth: 60, overflow: 'linebreak'},
          6: {columnWidth: 80, overflow: 'linebreak'},
          7: {columnWidth: 120, overflow: 'linebreak'},
          8: {columnWidth: 'auto', overflow: 'linebreak'}
        },
        drawRow: function (row, data) {
          doc.setFontStyle('bold')
          doc.setFontSize(12)
          if (row.raw[0] === '-'){
            doc.rect(data.settings.margin.left, row.y, data.table.width, 20, 'S');
            doc.autoTableText(markersMap.get(row.raw[1]), data.settings.margin.left + data.table.width / 2, row.y + row.height / 2, {
                halign: 'center',
                valign: 'middle'
            });
            data.cursor.y += 20
            return false
          } 
        }
      })
      doc.save('Appointments.pdf')      
    },
    initVenueLocationsMap(m, calendar) {
      console.log("Initialising the venue map..");
      const myLatlng = new window.google.maps.LatLng(34.95, 33.5833);
      const mapOptions = {
        zoom: 10,
        center: myLatlng,
        scrollwheel: true,
        mapTypeId: 'roadmap'
      };

      const map = new window.google.maps.Map(
        document.getElementById("venueLocationsMap"),
        mapOptions
      );

      console.log("Initialising the venue map.. DONE");
      window.venuesMap = map;
    },
    populateMap(event){
      console.log('-- populateMap --', arguments)
      console.log(document.getElementById('sla_radius').value)
      populateMap()
    },
    initCalendar($) {
      var self = this;
      var $calendar = $('#fullCalendar')
      $calendar.fullCalendar({
        // extras: 'Some extras',
        defaultView: 'listMonth',
        header: {
          left: "title",
          center:
            "listDay,agendaDay,listWeek,agendaWeek,listMonth",//month,agendaWeek,basicWeek,agendaDay,basicDay,listDay
          right: "prev,next today"
        },
        // validRange: {
        //     start: JSON.parse(sessionStorage.getItem('current_case_object')).instructing_party.instruction_received_at,
        // },
        buttonText: {
          today: "Today",
          month: "Month",
          agendaWeek: "Week",
          listDay: "Day(List)",
          agendaDay: "Day",
          //basicWeek: "Week(Basic)",
          //basicDay: "Day(Basic)",
          listWeek: "Week(List)",
          listMonth: "Month(List)"
        },
        defaultDate: this.selectedDate,
        selectable: true,
        selectHelper: true,
        // visibleRange: {
        //   start: '2020-09-20',
        //   end: '2022-09-20'
        // },
        views: {
          month: {
            // name of view
            titleFormat: "MMMM YYYY"
            // other view-specific options here
          },
          week: {
            titleFormat: " MMMM D YYYY"
          },
          day: {
            titleFormat: "D MMM YYYY"
          }
        },
        allDaySlot: false,
        slotDuration: "00:05:00",
        slotLabelInterval: "00:05:00",
        minTime: "05:00:00",
        maxTime: "22:00:00",
        timeFormat: "HH:mm",
        axisFormat: "HH:mm",
        timezone: "Europe/London",
        scrollTime: "08:00:00",
        navLinks: true, // can click day/week names to navigate views
        editable: true,
        eventLimit: true, // allow "more" link when too many events
        eventRender: function(event, element) {
          var tooltip_content = event.title;
          if (event.user) {
            tooltip_content += "\nAssigned to:\n" + event.user;
          }
          if (event.comment) {
            tooltip_content += "\nComment:\n" + event.comment;
          }
          if (event.appointment) {
            tooltip_content +=
              "\nCreated at:\n" + event.appointment.date_created;
          }
          if (event.details.expert_details) {
            tooltip_content +=
              "\n\nExpert's specialisations:\n" + event.details.expert_details.specialisations;
          }
          if (event.details.venue_details) {
            tooltip_content +=
              "\n\nVenue facilities:\n" + "\n - parking: " + event.details.venue_details.parking + "\n - disabled access: "+event.details.venue_details.disable_access + 
              "\n - lift access: "+event.details.venue_details.lift_access + "\n - child friendly: "+event.details.venue_details.child_friendly;
          }

          element.prop("title", tooltip_content);
        },
        eventClick: function(calEvent, jsEvent, view) {
          console.log(calEvent);
          //TODO: Handle the case when the slot is already taken..it should be done at the backend side 

          const current_case_object = JSON.parse(sessionStorage.getItem('current_case_object'))
          const selected_supported_product = sessionStorage.getItem('selected_supported_product')

          if (!current_case_object){
            // Delete slot:
            var booking_form_data = {}
            Swal.fire({
              title: "Delete Slot",
              html: '<div class="md-layout">'
                    + '<div class="md-layout-item md-size-100">'
                    +   '<div class="md-field md-theme-default md-required md-has-value">'
                    +     '<label for="cal_dialog_book_slot_datetime">Slot date and time</label>'
                    +     '<i class="md-icon md-icon-font md-icon-image md-date-icon md-theme-default">'
                    +       '<svg height="24" viewBox="0 0 24 24" width="24" xmlns="http://www.w3.org/2000/svg">'
                    +        '<path d="M17 12h-5v5h5v-5zM16 1v2H8V1H6v2H5c-1.11 0-1.99.9-1.99 2L3 19c0 1.1.89 2 2 2h14c1.1 0 2-.9 2-2V5c0-1.1-.9-2-2-2h-1V1h-2zm3 18H5V8h14v11z"></path>'
                    +        '<path d="M0 0h24v24H0z" fill="none"></path>'
                    +       '</svg>'
                    +     '</i>'
                    +     '<input autocomplete="__none__" type="text" id="cal_dialog_book_slot_datetime" readonly disabled required="required" class="md-input" aria-required="true" aria-invalid="false" value="'+calEvent.start.format("HH:mm")+" on "+calEvent.start.format("DD-MM-YYYY")+'"/>'
                    +   '</div>'
                    + '</div>'
                    + '<div class="md-layout-item md-size-100">'
                    +   '<div class="md-field md-theme-default md-required md-has-value">'
                    +     '<label for="cal_dialog_book_slot_expert">Expert</label>'
                    +     '<input autocomplete="__none__" type="text" id="cal_dialog_book_slot_expert" readonly disabled required="required" class="md-input" aria-required="true" aria-invalid="false" value="'+calEvent.details.expert+'"/>'
                    +   '</div>'
                    + '</div>'
                    + '<div class="md-layout-item md-size-100">'
                    +   '<div class="md-field md-theme-default md-required md-has-value">'
                    +     '<label for="cal_dialog_book_slot_venue">Venue</label>'
                    +     '<input autocomplete="__none__" type="text" id="cal_dialog_book_slot_venue" readonly disabled required="required" class="md-input" aria-required="true" aria-invalid="false" value="'+calEvent.details.venue+'"/>'
                    +   '</div>'
                    + '</div>'
                    + '<div class="md-layout-item md-size-100">'
                    +   '<div class="md-field md-theme-default md-disabled md-has-textarea">'
                    +     '<label for="cal_dialog_book_slot_note">Note</label>'
                    +     '<textarea data-vv-name="item.other" id="cal_dialog_book_slot_note" class="md-textarea">'
                    +     '</textarea>'
                    +   '</div>'
                    +'</div>',
              showCancelButton: true,
              confirmButtonClass: "md-button md-success",
              cancelButtonClass: "md-button md-danger",
              buttonsStyling: true,
              preConfirm: () => {
                booking_form_data.note = document.getElementById('cal_dialog_book_slot_note').value
              }
            }).then(result => {
              // Delete
              if (result.value) {
                console.log(calEvent)
                window.$http
                .create({headers: { 'Content-Type': 'application/json'}})
                .delete(window.url__calendar_appointmentslot+calEvent.id+'/')
                .then(response => {
                  Swal.fire("Good job!", "Slot booked!</br> Email notification sent to Claimant. </br> Email notification sent to Instructing party. </br> Email notification sent to Expert.", "success")
                  $("#fullCalendar").fullCalendar("refetchEvents")
                  })
                .catch(function(r) {
                  console.log(typeof(r), r)
                  // if 401 => route to login page..
                  if( 401 == r.request.status ){
                    window.location.href = '/'
                  }
                  if(r.response && r.response.data){
                    var error_message = ''
                    for (var prop in r.response.data) {
                      error_message += '</br>'+prop+': '+r.response.data[prop]
                    }
                    Swal.fire("Error", "The slot could not be updated.</br> "+error_message, "error")
                  } else {
                    Swal.fire("Error", "The slot could not be updated.</br> "+r.response, "error")
                  }            
                });
              }
            })
          } else if (calEvent.id){
            var report_types_html = '<select name="cal_dialog_book_slot_report_type" id="cal_dialog_book_slot_report_type" class="md-menu md-select" md-layout="box" md-input-placeholder="Medical report Type">'
            for (var i = 0; i < window.product_types.length; i++) {
              report_types_html += '<option class="md-list-item md-menu-item md-theme-default" value="'+window.product_types[i].id+'">'+window.product_types[i].name+'</option>'
             }
            report_types_html += '</select>'
                        
            var booking_form_data = {}
            Swal.mixin({
              confirmButtonText: 'Next &rarr;',
              showCancelButton: true,
              progressSteps: ['1', '2']
            }).queue([
              {
                title: "Book Appointment",
                html: '<div class="md-layout">'
                    + '<div class="md-layout-item md-size-100">'
                    +   '<div class="md-field md-theme-default md-required md-has-value">'
                    +     '<label for="cal_dialog_book_slot_datetime">Slot date and time</label>'
                    +     '<i class="md-icon md-icon-font md-icon-image md-date-icon md-theme-default">'
                    +       '<svg height="24" viewBox="0 0 24 24" width="24" xmlns="http://www.w3.org/2000/svg">'
                    +        '<path d="M17 12h-5v5h5v-5zM16 1v2H8V1H6v2H5c-1.11 0-1.99.9-1.99 2L3 19c0 1.1.89 2 2 2h14c1.1 0 2-.9 2-2V5c0-1.1-.9-2-2-2h-1V1h-2zm3 18H5V8h14v11z"></path>'
                    +        '<path d="M0 0h24v24H0z" fill="none"></path>'
                    +       '</svg>'
                    +     '</i>'
                    +     '<input autocomplete="__none__" type="text" id="cal_dialog_book_slot_datetime" readonly disabled required="required" class="md-input" aria-required="true" aria-invalid="false" value="'+calEvent.start.format("HH:mm")+" on "+calEvent.start.format("DD-MM-YYYY")+'"/>'
                    +   '</div>'
                    + '</div>'
                    + '<div class="md-layout-item md-size-100">'
                    +   '<div class="md-field md-theme-default md-required md-has-value">'
                    +     '<label for="cal_dialog_book_slot_expert">Expert</label>'
                    +     '<input autocomplete="__none__" type="text" id="cal_dialog_book_slot_expert" readonly disabled required="required" class="md-input" aria-required="true" aria-invalid="false" value="'+calEvent.details.expert+'"/>'
                    +   '</div>'
                    + '</div>'
                    + '<div class="md-layout-item md-size-100">'
                    +   '<div class="md-field md-theme-default md-required md-has-value">'
                    +     '<label for="cal_dialog_book_slot_venue">Venue</label>'
                    +     '<input autocomplete="__none__" type="text" id="cal_dialog_book_slot_venue" readonly disabled required="required" class="md-input" aria-required="true" aria-invalid="false" value="'+calEvent.details.venue+'"/>'
                    +   '</div>'
                    + '</div>'
                    + '<div class="md-layout-item md-size-100">'
                    +   '<div class="md-field md-theme-default md-required md-has-value">'
                    +     '<label for="cal_dialog_book_slot_case">Case</label>'
                    +     '<input autocomplete="__none__" type="text" id="cal_dialog_book_slot_case" readonly disabled required="required" class="md-input" aria-required="true" aria-invalid="false" value="'+sessionStorage.getItem('current_case_label')+'"/>'
                    +   '</div>'
                    + '</div>',
              showCancelButton: true,
              confirmButtonClass: "md-button md-success",
              cancelButtonClass: "md-button md-danger",
              buttonsStyling: true,
              },
              {
                width: `900px`,
                title: "A bit more details!",
                html: '<div class="md-layout-item md-size-100">'
                      +   '<div class="md-field md-theme-default md-required md-has-value">'
                      +     '<label for="cal_dialog_book_slot_report_type">Medical report type</label>'
                      +     report_types_html
                      +   '</div>'
                      + '</div>'
                      + '<div class="md-layout-item md-size-100">'
                      +   '<div class="md-field md-theme-default md-disabled md-has-value md-has-textarea">'
                      +     '<label for="cal_dialog_book_slot_note">Note</label>'
                      +     '<textarea data-vv-name="item.other" id="cal_dialog_book_slot_note" class="md-textarea">'
                      +     '</textarea>'
                      +   '</div>'
                      +'</div>'
                      +'<div class="md-layout-item md-size-100" style="text-align:left">'
                      +'<input type="checkbox" class="md-checkbox" name="who_to_email_checkboxes" value="email_claimant" checked>'
                      +'<label>Email Claimant: ' + current_case_object.claimant.email + '</label>'
                      +'</input>'
                      +'</div>'
                      +'<div class="md-layout-item md-size-100" style="text-align:left">'
                      +'<input type="checkbox" class="md-checkbox" name="who_to_email_checkboxes" value="email_instructing_party" checked>'
                      +'<label>Email Instructing Party File Handler: ' + current_case_object.instructing_party.file_handler_email + '</label>'
                      +'</input>'
                      +'</div>'
                      +'<div class="md-layout-item md-size-100" style="text-align:left">'
                      +'<input type="checkbox" class="md-checkbox" name="who_to_email_checkboxes" value="email_expert" checked>'
                      +'<label>Email Expert: ' + calEvent.details.expert_email + '</label>'
                      +'</input>'
                      +'</div>'
                      +'<div class="md-layout-item md-size-100">'
                      +   '<div class="md-field md-theme-default md-has-value md-has-textarea">'
                      +     '<label>Additional emails seperated by a ,</label>'
                      +     '<textarea data-vv-name="item.other" id="cal_dialog_book_slot_additional_emails" class="md-textarea">'
                      +     '</textarea>'
                      +   '</div>'
                      +'</div>',
                  showCancelButton: true,
                  confirmButtonClass: "md-button md-success",
                  confirmButtonText: "Book it",
                  cancelButtonClass: "md-button md-danger",
                  buttonsStyling: true,
                  preConfirm: () => {
                    booking_form_data.note = document.getElementById('cal_dialog_book_slot_note').value
                    booking_form_data.report_type = document.getElementById('cal_dialog_book_slot_report_type').value
                    booking_form_data.email_list = []
                    booking_form_data.additional_emails = document.getElementById('cal_dialog_book_slot_additional_emails').value
                    document.getElementsByName('who_to_email_checkboxes').forEach(element => {
                      if(element.checked){
                        booking_form_data.email_list.push(element.value)
                      }
                    });
                  }
              }

            ]).then(result => {
              if (result.value) {
                console.log(calEvent)
                console.log(this.selected_product)
                console.log('TESSTINGGGGGG')
                // this.claimantAppointmentNotificationPDF(calEvent, false)
                window.$http
                .create({headers: { 'Content-Type': 'application/json'}})
                .put(window.url__calendar_book_slot, {'slot': calEvent.id, 'case': current_case_object.id, 'note': booking_form_data.note, 'report_type': selected_supported_product,
                                                      'email_list': booking_form_data.email_list, 'additional_emails': booking_form_data.additional_emails })
                .then(response => {
                  console.log(response)
                  var booking_msg = 'Slot booked!</br><div class="md-field md-theme-default"><ul style="text-align:left">'

                  var email_notifications = []

                  if ( response.data.email_expert ) {
                    email_notifications.push('Expert')
                  }
                  if ( response.data.email_instructing_party ) {
                    email_notifications.push('Instructing party')
                  }
                  if ( response.data.email_claimant ) {
                    email_notifications.push('Claimant')
                  }
                  if ( response.data.additional_emails ) {
                    email_notifications.push('additional recipients')
                  }

                  if( email_notifications && email_notifications.length > 0 ){
                    booking_msg += '<li>'+'Email notifications sent to: '+email_notifications.join(', ')+'.</li>'
                  }

                  if ( response.data.invoice ) {
                    booking_msg += '<li><a href="/invoice/edit/'+response.data.invoice+'">Proforma invoice: '+response.data.invoice+'</a></li>'
                  }

                  booking_msg += '</ul></div>'

                  if (response.data.medical_report) {
                    booking_msg += '</br> Dummy ' + response.data.medical_report + ' created. '
                  }

                  Swal.fire("Good job!", booking_msg, "success")
                  $("#fullCalendar").fullCalendar("refetchEvents")
                })
                .catch(function(r) {
                  console.log(typeof(r), r)
                  // if 401 => route to login page..
                  if( 401 == r.request.status ){
                    window.location.href = '/'
                  }
                  if(r.response && r.response.data){
                    var error_message = ''
                    for (var prop in r.response.data) {
                      error_message += '</br>'+prop+': '+r.response.data[prop]
                    }
                    Swal.fire("Error", "The slot could not be updated.</br> "+error_message, "error")
                  } else {
                    Swal.fire("Error", "The slot could not be updated.</br> "+r.response, "error")
                  }
                });
              }
            })
          }
        },
        select: function(start, end) {

          var selectedExpert = sessionStorage.getItem("appointments_calendar_selectedExpert")
          var selectedVenue = sessionStorage.getItem("appointments_calendar_selectedVenue")
          if (!selectedExpert || !selectedVenue){
             Swal.fire({
              title: "Error",
              text: 'Please select the Expert and the Venue before creating the slot.',
              type: "error",
              confirmButtonClass: "md-button md-success btn-fill",
              buttonsStyling: false
            });
            return
          }
          
          var slot_form_data = {}
          Swal.fire({
            title: "Create the slot",
            html: '<div class="md-layout">'
                  + '<div class="md-layout-item md-size-100">'
                  +   '<div class="md-field md-theme-default md-required md-has-value">'
                  +     '<label for="cal_dialog_book_slot_datetime">Slot date and time</label>'
                  +     '<i class="md-icon md-icon-font md-icon-image md-date-icon md-theme-default">'
		              +       '<svg height="24" viewBox="0 0 24 24" width="24" xmlns="http://www.w3.org/2000/svg">'
		              +        '<path d="M17 12h-5v5h5v-5zM16 1v2H8V1H6v2H5c-1.11 0-1.99.9-1.99 2L3 19c0 1.1.89 2 2 2h14c1.1 0 2-.9 2-2V5c0-1.1-.9-2-2-2h-1V1h-2zm3 18H5V8h14v11z"></path>'
		              +        '<path d="M0 0h24v24H0z" fill="none"></path>'
		              +       '</svg>'
                  +     '</i>'
                  +     '<input autocomplete="__none__" type="text" id="cal_dialog_book_slot_datetime" readonly disabled required="required" class="md-input" aria-required="true" aria-invalid="false" value="'+start.format("HH:mm")+" on "+start.format("DD-MM-YYYY")+'"/>'
                  +   '</div>'
                  + '</div>'
                  + '<div class="md-layout-item md-size-100">'
                  +   '<div class="md-field md-theme-default md-required md-has-value">'
                  +     '<label for="cal_dialog_book_slot_expert">Expert</label>'
                  +     '<input autocomplete="__none__" type="text" id="cal_dialog_book_slot_expert" readonly disabled required="required" class="md-input" aria-required="true" aria-invalid="false" value="'+selectedExpert+'"/>'
                  +   '</div>'
                  + '</div>'
                  + '<div class="md-layout-item md-size-100">'
                  +   '<div class="md-field md-theme-default md-required md-has-value">'
                  +     '<label for="cal_dialog_book_slot_venue">Venue</label>'
                  +     '<input autocomplete="__none__" type="text" id="cal_dialog_book_slot_venue" readonly disabled required="required" class="md-input" aria-required="true" aria-invalid="false" value="'+selectedVenue+'"/>'
                  +   '</div>'
                  + '</div>'
                  + '<div class="md-layout-item md-size-100">'
                  +   '<div class="md-field md-theme-default md-disabled md-has-textarea">'
                  +     '<label for="cal_dialog_create_slot_note">Note</label>'
                  +     '<textarea data-vv-name="item.other" id="cal_dialog_create_slot_note" class="md-textarea">'
                  +     '</textarea>'
                  +   '</div>'
                  +'</div>',
            showCancelButton: true,
            confirmButtonClass: "md-button md-success",
            cancelButtonClass: "md-button md-danger",
            buttonsStyling: true,
            preConfirm: () => {
              slot_form_data.note = document.getElementById('cal_dialog_create_slot_note').value
            }
          }).then(result => {
            if (result.value) {
              window.$http
              .create({headers: { 'Content-Type': 'application/json'}})
              .put(window.url__calendar_appointmentslot, {'datetime': start, 'expert': selectedExpert, 'venue': selectedVenue, 'note': slot_form_data.note, 'checkboxes': slot_form_data.checkboxes})
              .then(response => {
                Swal.fire("Good job!", "Slot Created!", "success")
                $("#fullCalendar").fullCalendar("refetchEvents")
                })
              .catch(function(r) {
                console.log(typeof(r), r)
                // if 401 => route to login page..
                if( 401 == r.request.status ){
                  window.location.href = '/'
                }
                if(r.response && r.response.data){
                  var error_message = ''
                  for (var prop in r.response.data) {
                    error_message += '</br>'+prop+': '+r.response.data[prop]
                  }
                  Swal.fire("Error", "The slot could not be updated.</br> "+error_message, "error")
                } else {
                  Swal.fire("Error", "The slot could not be updated.</br> "+r.response, "error")
                }            
              });
            }
          })
        },
        eventAfterAllRender: function(view) {
          populateMap()
        },
        // color classes: [ event-blue | event-azure | event-green | event-orange | event-red ]
        // events: self.events
        events: {
          url: window.url__calendar_events,
          cache: false,
          headers: {
            Authorization: "JWT " + sessionStorage.getItem("jwt")
          },
          data: function() {
              const current_case_object = JSON.parse(sessionStorage.getItem('current_case_object'))
              if (current_case_object && sessionStorage.getItem("selected_supported_product") !== '-'){
                var criteria = {appointments: JSON.parse(sessionStorage.getItem("appointments_calendar_showAppointments")) ? 1 : 0}

                if (sessionStorage.getItem("appointments_calendar_selectedExperts")){
                  criteria.expert = sessionStorage.getItem("appointments_calendar_selectedExperts")
                }
                if (sessionStorage.getItem("appointments_calendar_selectedVenue")){
                  criteria.venue = sessionStorage.getItem("appointments_calendar_selectedVenue")
                }
                if (sessionStorage.getItem("selected_supported_product")){
                  criteria.selected_supported_product = sessionStorage.getItem("selected_supported_product")
                }
                if (sessionStorage.getItem("map_radius")){
                  criteria.map_radius = sessionStorage.getItem("map_radius")
                }

                if($('#venue_parking').parents('.md-checked').length){
                  criteria.venue_parking = true
                }

                if($('#venue_disable_access').parents('.md-checked').length){
                  criteria.venue_disable_access = true
                }

                if($('#venue_lift_access').parents('.md-checked').length){
                  criteria.venue_lift_access = true
                }

                if($('#venue_child_friendly').parents('.md-checked').length){
                  criteria.venue_child_friendly = true
                }
                criteria.recommended_appointment_range_start = current_case_object.instructions.recommended_appointment_range_start
                criteria.recommended_appointment_range_end = current_case_object.instructions.recommended_appointment_range_end
                criteria.instruction_received_at = current_case_object.instructing_party.instruction_received_at
                criteria.claimant_postcode = current_case_object.claimant.postcode
                criteria.vulnerable = current_case_object.claimant.vulnerable
                criteria.underage = current_case_object.claimant.underage
                if($('#requests').parents('.md-checked').length){
                  criteria.what_to_show = 'requests'
                }
                if($('#slots').parents('.md-checked').length){
                  criteria.what_to_show = 'slots'
                }
                if($('#all').parents('.md-checked').length){
                  criteria.what_to_show = 'all'
                }
                console.log("criteria:",criteria)
                return criteria
              }else{
                var criteria = {empty: true}
                return criteria
              }
          }
        }
      });
      // this.calendar.vuecontext = $
      // console.log('*****',this.calendar.vuecontext)
    }
  },
  // created() {
    // if(!this.selectedExpert){
    //   this.setCurrentExpert(sessionStorage.getItem("appointments_calendar_selectedExpert"))
    // }
    // if(!this.selectedVenue){
    //   this.setCurrentExpert(sessionStorage.getItem("appointments_calendar_selectedVenue"))
    // }
      // selectedDate: JSON.parse(sessionStorage.getItem("appointments_selectedDate")),
      // selectedExpert: sessionStorage.getItem("appointments_calendar_selectedExpert"),
      // selectedVenue: sessionStorage.getItem("appointments_calendar_selectedVenue"),
      // showAppointments: JSON.parse(sessionStorage.getItem("appointments_calendar_showAppointments")),

  // },
  async mounted() {
    NProgress.start()
    console.log('5')
    window.$ = window.jQuery = $;
    var self = this;

    // this.$http.get(this.url__specialisation)
    //   .then(response => {
    //     if (response.data) {
    //       this.specialisations = response.data;
    //     }
    //   })
    //   .catch(function (error) {
    //     console.error(error.response);
    //   });

      const current_case_object = JSON.parse(sessionStorage.getItem('current_case_object'))
      console.log(current_case_object)

      this.$http
        .get(this.url__product_types )
        .then(response => {

            // we only need ones listed as recommended.. and maybe only the active ones too: product.active === true
            window.product_types = response.data.filter(product => current_case_object.instructing_party.products.indexOf(product.id) != -1)
            this.product_types = window.product_types            
            
        })
        .catch(function(error) {
            console.error(error.response);
        })

    var calendarPromise = new Promise(function(resolve, reject) {
      self.initCalendar($);
      resolve(self.calendar);
    }).then(function(v) {
      console.log(' ------ ',v)
      // calendar.prototype.$http = self.$http
      // console.log(calendar.$http)
      GoogleMapsLoader.load(google => {
        self.initVenueLocationsMap(google, v);
        NProgress.done()
      });
    });
  },
  watch: {
    selected_attachments: function(val){
      sessionStorage.setItem('appointments_selected_attachments', JSON.stringify(this.selected_attachments))
    },
    // selected_specialisations: function(val) {
    //   console.log('selected_specialisations:',val)
    //   console.log(this.experts_with_specialisations)
    //   this.selected_experts = this.experts_with_specialisations.filter( function(item) {
    //     let current_selection = new Set(val);
    //     let experts_specialisations = new Set(item.specialisations);
    //     console.log(experts_specialisations)
    //     let intersection = new Set(
    //         [...current_selection].filter(x => experts_specialisations.has(x)))
    //     return intersection.size === current_selection.size ? true : false
    //   }).map(x => x.label);
    //   console.log("Experts matching specialisations:",this.selected_experts.length)
    //   sessionStorage.removeItem("appointments_calendar_selectedExperts")
    //   sessionStorage.setItem("appointments_calendar_selectedExperts", this.selected_experts)
    //   var calendar = $("#fullCalendar")
    //   calendar.fullCalendar('removeEvents')
    //   calendar.fullCalendar("refetchEvents")
        
    //   console.log(this.selected_experts)

    // },
    // venue_parking: function(val) {
    //   console.log('venue_parking:',val)
    //   sessionStorage.removeItem("appointments_calendar_venue_parking")
    //   sessionStorage.setItem("appointments_calendar_venue_parking", val)
    //   var calendar = $("#fullCalendar")
    //   calendar.fullCalendar('removeEvents')
    //   calendar.fullCalendar("refetchEvents")
    //   cleanupMarkers()
    // },
    // venue_disable_access: function(val) {
    //   console.log('venue_disable_access:',val)
    //   sessionStorage.removeItem("appointments_calendar_venue_disable_access")
    //   sessionStorage.setItem("appointments_calendar_venue_disable_access", val)
    //   var calendar = $("#fullCalendar")
    //   calendar.fullCalendar('removeEvents')
    //   calendar.fullCalendar("refetchEvents")
    //   cleanupMarkers()
    // },
    // venue_lift_access: function(val) {
    //   console.log('venue_lift_access:',val)
    //   sessionStorage.removeItem("appointments_calendar_venue_lift_access")
    //   sessionStorage.setItem("appointments_calendar_venue_lift_access", val)
    //   var calendar = $("#fullCalendar")
    //   calendar.fullCalendar('removeEvents')
    //   calendar.fullCalendar("refetchEvents")
    //   cleanupMarkers()
    // },
    // venue_child_friendly: function(val) {
    //   console.log('venue_child_friendly:',val)
    //   sessionStorage.removeItem("appointments_calendar_venue_child_friendly")
    //   sessionStorage.setItem("appointments_calendar_venue_child_friendly", val)
    //   var calendar = $("#fullCalendar")
    //   calendar.fullCalendar('removeEvents')
    //   calendar.fullCalendar("refetchEvents")
    //   cleanupMarkers()
    // },
    what_to_show: function(val) {
      window.what_to_show = val
      console.log('what_to_show: ', val)
      
      // Vue.nextTick(function () {
      //   $("#fullCalendar").fullCalendar('removeEvents')
      //   Vue.nextTick(function () {
      //     NProgress.start()
      //     console.log('6')
      //     $("#fullCalendar").fullCalendar("refetchEvents")
      //   })
      // })
    },
    venue_parking: function(val) {
      window.venue_parking = val
      console.log('venue_parking: ', val)
      
      // Vue.nextTick(function () {
      //   $("#fullCalendar").fullCalendar('removeEvents')
      //   Vue.nextTick(function () {
      //     NProgress.start()
      //     console.log('7')
      //     $("#fullCalendar").fullCalendar("refetchEvents")
      //   })
      // })
    },
    venue_disable_access: function(val) {
      window.venue_disable_access = val
      // Vue.nextTick(function () {
      //   $("#fullCalendar").fullCalendar('removeEvents')
      //   Vue.nextTick(function () {
      //     NProgress.start()
      //     console.log('8')
      //     $("#fullCalendar").fullCalendar("refetchEvents")
      //   })
      // })
    },
    venue_lift_access: function(val) {
      window.venue_lift_access = val
      // Vue.nextTick(function () {
      //   $("#fullCalendar").fullCalendar('removeEvents')
      //   Vue.nextTick(function () {
      //     NProgress.start()
      //     console.log('9')
      //     $("#fullCalendar").fullCalendar("refetchEvents")
      //   })
      // })
    },
    venue_child_friendly: function(val) {
      window.venue_child_friendly = val
      // Vue.nextTick(function () {
      //   $("#fullCalendar").fullCalendar('removeEvents')
      //   Vue.nextTick(function () {
      //     NProgress.start()
      //     console.log('10')
      //     $("#fullCalendar").fullCalendar("refetchEvents")
      //   })
      // })
    },
    selected_supported_product: function(val) {
      if (val && val !== '-') {
          this.$http
          .get(this.url__experts_with_supported_products)
          .then(response => {
            this.experts_with_supported_products = response.data;
            const current_case_object = JSON.parse(sessionStorage.getItem('current_case_object'))
            var warning_html = ''
            if (current_case_object.instructions.recommended_appointment_range_start){
              warning_html += `<br><span style="font-size: 20px"><b>Appointment After the: <u>${moment(current_case_object.instructions.recommended_appointment_range_start).format('DD/MM/YYYY')}</u></b></span>`
            }
            if (current_case_object.instructions.recommended_appointment_range_end){
              warning_html += `<br><span style="font-size: 20px"><b>Appointment Before the: <u>${moment(current_case_object.instructions.recommended_appointment_range_end).format('DD/MM/YYYY')}</u></b></span>`
            }
            if (warning_html){
              warning_html = '<b><span style="font-size: 25px">You have special Intructions!</span></b><br>' + warning_html
              Swal.fire({
                position: 'center-center',
                type: 'warning',
                title: 'Please Note',
                html: warning_html,
                showConfirmButton: true,
              })
            }
            
            this.$http
              .get(this.url__is_product_third_party + val + '/' )
              .then(response => {
                  if (response.data.is_third_party){
                    this.third_party_companies = response.data.companies
                    this.show_third_party_booking = true
                    this.show_normal_booking = false
                    return
                  }else{
                    this.show_third_party_booking = false
                    this.show_normal_booking = true
                  }
              })
              .catch(function(error) {
                  console.error(error.response);
                  Swal.fire(
                      'Error',
                      error.response,
                      'error'
                  )
              });
            // NProgress.start()
            console.log('1')
            console.log('selected_supported_product:',val)
            sessionStorage.removeItem('selected_supported_product')
            sessionStorage.setItem('selected_supported_product', this.selected_supported_product)
            console.log(this.experts_with_supported_products)
            if (this.experts_with_supported_products){
              this.selected_experts = this.experts_with_supported_products.filter( function(item) {
                let current_selection = new Set([val]);
                let experts_supported_products = new Set(item.supported_products);
                let intersection = new Set(
                    [...current_selection].filter(x => experts_supported_products.has(x)))
                return intersection.size === current_selection.size && current_selection.size > 0 ? true : false
              }).map(x => x.id);
              console.log("Experts matching supported_products:",this.selected_experts.length)
              sessionStorage.removeItem("appointments_calendar_selectedExperts")
              if (this.selectedExpert && this.selected_experts.includes(this.selectedExpert)){
                sessionStorage.setItem("appointments_calendar_selectedExperts", [this.selectedExpert])
                console.log('this.selectedExpert', [this.selectedExpert])
              }else if (this.selectedExpert){
                sessionStorage.setItem("appointments_calendar_selectedExperts", [])
              }else{
                sessionStorage.setItem("appointments_calendar_selectedExperts", this.selected_experts)
              }
              // var calendar = $("#fullCalendar")
              // calendar.fullCalendar('removeEvents')
              // calendar.fullCalendar("refetchEvents")
              cleanupMarkers()
                
              console.log(this.selected_experts)
            }
          })
          .catch(function(error) {
            console.error(error.response);
          });
      } else {
        console.log('No product selected!')
        sessionStorage.removeItem("selected_supported_product")
        sessionStorage.removeItem("appointments_calendar_selectedExperts")
        sessionStorage.setItem("appointments_calendar_selectedExperts", '')
        // var calendar = $("#fullCalendar")
        // calendar.fullCalendar('removeEvents')
        // calendar.fullCalendar("refetchEvents")
        cleanupMarkers()
      }

    },
    // selectedDate: function(val) {
    //   var calendar = $('#fullCalendar')
    //   console.log('selectedDate:',this.selectedDate)
    //   sessionStorage.removeItem("appointments_selectedDate")
    //   sessionStorage.setItem("appointments_selectedDate", JSON.stringify(this.selectedDate))
    //   // this.selectedDate = moment(val).format('yyyy-mm-dd')
    //   // this.current_start_date = moment(this.selectedDate).format('DD/MM/YYYY')
    //   // this.current_end_date = moment(this.selectedDate).add(1, 'months').format('DD/MM/YYYY')
    //   // calendar.fullCalendar("gotoDate", val)
    //   // calendar.fullCalendar('removeEvents')
      
    //   // calendar.fullCalendar("refetchEvents")
    //   // calendar.fullCalendar('gotoDate', this.selectedDate)
    //   this.selectedDate = moment(val).format('DD/MM/YYYY')
    //   calendar.fullCalendar("refetchEvents")
    //   cleanupMarkers()
    // },
    selectedExpert: function(val) {
      console.log('selectedExpert:',val, this.selectedExpert)
      sessionStorage.removeItem("appointments_calendar_selectedExpert")
      sessionStorage.setItem("appointments_calendar_selectedExpert", this.selectedExpert)
      this.setCurrentExpert(this.selectedExpert)
      const local_selected_supported_product = this.selected_supported_product
      if (val){
        if (this.experts_with_supported_products === null){
          this.$http
          .get(this.url__experts_with_supported_products)
          .then(response => {
            this.experts_with_supported_products = response.data;
            this.selected_experts = this.experts_with_supported_products.filter( function(item) {
            let current_selection = new Set([local_selected_supported_product]);
            let experts_supported_products = new Set(item.supported_products);
            let intersection = new Set(
                [...current_selection].filter(x => experts_supported_products.has(x)))
              return intersection.size === current_selection.size && current_selection.size > 0 ? true : false
            }).map(x => x.label);
            console.log("Experts matching supported_products:",this.selected_experts.length)
            sessionStorage.removeItem("appointments_calendar_selectedExperts")
            if (this.selected_experts.includes(this.selectedExpert)){
              sessionStorage.setItem("appointments_calendar_selectedExperts", [this.selectedExpert])
              console.log('this.selectedExpert', [this.selectedExpert])
            }else if (this.selectedExpert){
              sessionStorage.setItem("appointments_calendar_selectedExperts", [])
            }
          })
          .catch(function(error) {
            console.error(error.response);
          });
        }
      }else{
        sessionStorage.setItem("appointments_calendar_selectedExperts", this.selected_experts)
      }
      // var calendar = $("#fullCalendar")
      // calendar.fullCalendar('removeEvents')
      // calendar.fullCalendar("refetchEvents")
      cleanupMarkers()
    },
    selectedVenue: function(val) {
      console.log('selectedVenue:',this.selectedVenue)
      sessionStorage.removeItem("appointments_calendar_selectedVenue")
      sessionStorage.setItem("appointments_calendar_selectedVenue", this.selectedVenue)
      this.setCurrentVenue(this.selectedVenue)
      // var calendar = $("#fullCalendar")
      // calendar.fullCalendar('removeEvents')
      // calendar.fullCalendar("refetchEvents")
      cleanupMarkers()
    },
    showAppointments: function(val) {
      console.log('showAppointments:',val, this.showAppointments)
      sessionStorage.removeItem("appointments_calendar_showAppointments")
      sessionStorage.setItem("appointments_calendar_showAppointments", JSON.stringify(this.showAppointments))
      var calendar = $("#fullCalendar")
      calendar.fullCalendar("refetchEvents")
    },
    currentCase: function(val) {
      console.log("Current case has changed to:", val)
      if (val === null){
        console.log("Resetting the markers..")
        cleanupMarkers()
      }
      $("#fullCalendar").fullCalendar('removeEvents')
      NProgress.start()
      console.log('1')
      $("#fullCalendar").fullCalendar("refetchEvents")
    },
    sla_radius: function(val) {
      console.log("Current sla radius has changed to:", val)
      window.sla_radius = val
      sessionStorage.setItem("map_radius", val)
      // $("#fullCalendar").fullCalendar('removeEvents')
      // NProgress.start()
      // console.log('2')
      // $("#fullCalendar").fullCalendar("refetchEvents")
    },
  },
  computed: {
    ...mapGetters([
      'currentCase',
      'currentCaseLabel',
      'currentExpert',
      'currentVenue'
    ])
  }
};
</script>

<style lang="scss" scoped>
#fullCalendar {
  min-height: 300px;
}

.md-card-calendar {
  .md-card-content {
    padding: 0 !important;
  }
}

.text-center {
  text-align: center;
}

.map{
      height: 600px;
      width: 100%;
    }

.card-map {
    min-height: 350px;
    .map{
      height: 600px;
      width: 100%;
    }
  }

.swal-wide {
  width: 850px !important;
}

// Base Colors
$shade-10: #2c3e50 !default;
$shade-1: #d7dcdf !default;
$shade-0: #fff !default;
$teal: #1abc9c !default;

#app{
  width: 400px;
  background: #eee;
  margin: 0 auto;
}

// Range Slider
// $range-width: 100% !default;

$range-handle-color: $shade-10 !default;
$range-handle-color-hover: $teal !default;
$range-handle-size: 20px !default;

$range-track-color: $shade-1 !default;
$range-track-height: 10px !default;

$range-label-color: $shade-10 !default;
$range-label-width: 60px !default;

// .range-slider {
//   width: $range-width;
// }

.range-slider__range {
  -webkit-appearance: none;
  width: 500px;
  height: $range-track-height;
  border-radius: 5px;
  background: $range-track-color;
  outline: none;
  padding: 0;
  margin: 0;

  // Range Handle
  &::-webkit-slider-thumb {
    appearance: none;
    width: $range-handle-size;
    height: $range-handle-size;
    border-radius: 50%;
    background: $range-handle-color;
    cursor: pointer;
    transition: background .15s ease-in-out;

    &:hover {
      background: $range-handle-color-hover;
    }
  }

  &:active::-webkit-slider-thumb {
    background: $range-handle-color-hover;
  }

  &::-moz-range-thumb {
    width: $range-handle-size;
    height: $range-handle-size;
    border: 0;
    border-radius: 50%;
    background: $range-handle-color;
    cursor: pointer;
    transition: background .15s ease-in-out;

    &:hover {
      background: $range-handle-color-hover;
    }
  }

  &:active::-moz-range-thumb {
    background: $range-handle-color-hover;
  }
  

}
.low .-webkit-slider-thumb {
    background: red;
}

::-moz-range-track {
    background: $range-track-color;
    border: 0;
}

input::-moz-focus-inner,
input::-moz-focus-outer { 
  border: 0; 
}

</style>
