<template>
  <div>
        <div class="md-layout">
            <table class="attachmentTable" style="width:100%">
                <tr>
                    <th>#</th>
                    <th>Date created</th>
                    <th>Created by</th>
                    <th>Type</th>
                    <th>Logging</th>
                    <th>Date Request Received</th>
                    <th>Specific HTML Content</th>
                    <th>Failed Checks</th>
                    <th>View</th>
                    <th>Completed?</th>
                    <th>Resend</th>
                    <th>Delete</th>
                </tr>
                <tr v-for="(request, index) in this.appointmentData.requests" v-bind:key="index">
                    <td>{{index + 1}}</td>
                    <td>{{request.date_created | changeDateTimeFilter}}</td>
                    <td>{{request.created_by}}</td>
                    <td>{{request.type}}</td>
                    <td style="white-space: pre-line; font-size: 13px">{{request.logging}}</td>
                    <td>{{request.date_request_received | changeDateFilter}}</td>
                    <td style="white-space: pre-line">{{request.specific_html_content}}</td>
                    <td><md-button class="md-icon-button md-just-icon md-info" v-on:click="quality_assurance_swal(request.quality_assurance_failed_checks)"><md-icon>touch_app</md-icon></md-button></td>
                    <td><md-button v-if="request.attachments.length > 0" class="md-primary" v-on:click="viewAttachment(request.attachments[request.attachments.length -1].id)" :id="request.attachments[request.attachments.length -1].id">View</md-button></td>
                    <td v-if="request.completed"><md-button class="md-danger" v-on:click="completeRequest(request.id, false)">Unmark Completed</md-button></td>
                    <td v-else><md-button class="md-success" v-on:click="completeRequest(request.id, true)">Mark Completed</md-button></td>
                    <td><md-button title="Click to Resend Request" class="md-success" v-on:click="send_email(request)"><md-icon class="md-round md-just-icon md-transparent">send</md-icon></md-button></td>
                    <td><md-button title="Delete request" class="md-danger" v-on:click="deleteRequest(request.id)">Delete</md-button></td>
                </tr>
            </table>
        </div>
    <div class="md-layout-item md-size-100">
      <md-card>
        <md-card-header class="md-card-header-icon md-card-header-green">
          <div class="card-icon">
            <md-icon class="md-size-3x">how_to_reg</md-icon>
            <label style="font-size: 20px" >Request to <b>{{appointmentData.slot.expert}}</b></label>
          </div>
        </md-card-header>

        <div class="md-dialog">
            <div class="md-dialog-container"></div>
        </div>

        <md-card-content>
            <div class="md-layout-item inputBox">
                <label class="label-style">Select Request Type</label>
                <model-list-select
                    required
                    style="position: relative !important;z-index: 1 !important;"
                    :list="request_types_filtered"
                    v-model="selected_request_type"
                    option-text="type"
                    option-value="type"
                    placeholder="Select Request Type">
                </model-list-select>
            </div>
            <br>

        <div class="md-layout-item md-size-100 inputBox">
            <label class="label-style">Date Request received by IP</label>
            <br>
            <date-picker
                class="custom-datepicker"
                v-model="date_request_received"
                lang="en"
                type="date"
                format="DD-MM-YYYY">
            </date-picker>
        </div>
        <br>

        <div class="md-layout-item md-size-100 inputBox">
            <label class="label-style">Select Attachments</label>
            <div v-for="item in outputData.inputItems" :key="item.id">
                <md-checkbox
                    style="zoom:1.2;"
                    class="md-layout-item md-size-100"
                    v-if="item.visible"
                    v-model="item.selected">
                    <span style="color: blue"><u>FILE TYPE</u></span>: <b>{{item.type}}</b>&nbsp;&nbsp;&nbsp;<span style="color: blue"><u>UPLOAD DATETIME</u></span>: <b>{{item.date_created}}</b><br> <span style="color: blue"><u>FILENAME</u></span>: <b>{{item.filename}}</b>
                </md-checkbox>
            </div>
        </div>

        <div class="md-layout-item inputBox">
            <label class="label-style">Upload Email/Letter by Instructing Party</label>
            <br>
            <input style="font-size: 15px" type="file" id="file" ref="file" v-on:change="handleFileUpload()"/>
        </div>

        <div class="md-layout-item inputBox">
            <label class="label-style">CC:</label>
            <md-chips style="font-size: 15px" v-model="additional_emails" md-deletable md-check-duplicated class="md-primary" md-placeholder="Add emails and press enter..."></md-chips>
        </div>

        <div class="md-layout-item md-size-100" style="text-align: center">
            <md-button style="font-size: 30px" v-on:click="regards_to_prognosis_check(null)">SEND Email and Attachments</md-button>
        </div>
        </md-card-content>


      </md-card>
    </div>
  </div>
</template>
<script>
import { mapActions } from 'vuex'
import { mapGetters } from 'vuex'
import DatePicker from 'vue2-datepicker'
import Swal from "sweetalert2"
import moment from 'moment'
import { ModelListSelect } from 'vue-search-select';

var jsPDF = require('jspdf')
require('jspdf-autotable')
export default {
  components: {
    DatePicker,
    ModelListSelect
  },
  props: {
        id: Number,
        appointmentData: null,
    },
    filters: {
      changeDateTimeFilter:
          function (value) {
              return moment(value).format('DD/MM/YYYY HH:mm')
          },
      changeDateFilter:
          function (value) {
              var date = moment(value).format('DD/MM/YYYY')
              if (date === 'Invalid date'){
                  return 'N/A'
              }else{
                  return date
              }
          }
      },
  data() {
    return {
        regards_to_prog: false,
        parsed_requests: [],
        date_request_received: null,
        additional_emails: [],
        sent_to_email: null,
        specific_html_content: null,
        inputData: [],
        selected_documents: [],
        outputData: {filter: '', inputItems: []},
        all_attachments: [],
        selected_request_type: '',
        notes: '',
        file: '',
        filtered_request_types: [],
        filter_selection: '',
        request_types_filtered: [
            {type: 'Amendment of MEDCO GP Medical Report'},
            {type: 'Amendment of Re-examination(Report Rejected) MEDCO GP Medical Report'},
            {type: 'Amendment of Re-examination(Prognosis Exceeded) MEDCO GP Medical Report'},
            {type: 'Amendment of Non-medco GP Medical Report'},
            {type: 'Amendment of Re-examination (Report Rejected) Non-medco GP Medical Report'},
            {type: 'Amendment of Re-examination (Prognosis Exceeded) Non-medco GP Medical Report'},
            {type: 'Amendment of Specialist Orthopaedic Medical Report'},
            {type: 'Amendment of Re-examination (Report Rejected) Specialist Orthopaedic Medical Report'},
            {type: 'Amendment of Re-examination(Prognosis Exceeded) Specialist Orthopaedic Medical Report'},
            {type: 'Amendment of Specialist Psychological Medical Report'},
            {type: 'Amendment of Re-examination (Report Rejected) Specialist Psychological Medical Report'},
            {type: 'Amendment of Re-examination (Prognosis Exceeded) Specialist Psychological Medical Report'},
            {type: 'Amendment of Specialist ENT Report'},
            {type: 'Amendment of Specialist Surgeon'},
            {type: 'Amendment of Specialist Dental Report'},
            {type: 'Amendment of Specialist Gynaecology Report'},
            {type: 'Amendment of Specialist Neurology Report'},
            {type: 'Amendment of Holiday Illness Medical Report'},
            {type: 'Amendment of Rehabilitation Physiotherapy Initial Assessment Report'},
            {type: 'Amendment of Rehabilitation Physiotherapy Final Discharge Report'},
            {type: 'Amendment of Other Medical Report (to type)'},
            {type: 'Amendment with Review of Records of MEDCO GP Medical Report'},
            {type: 'Amendment with Review of Records of Re-examination(Report Rejected) MEDCO GP Medical Report'},
            {type: 'Amendment with Review of Records of Re-examination(Prognosis Exceeded) MEDCO GP Medical Report'},
            {type: 'Amendment with Review of Records of Non-medco GP Medical Report'},
            {type: 'Amendment with Review of Records of Re-examination (Report Rejected) Non-medco GP Medical Report'},
            {type: 'Amendment with Review of Records of Re-examination (Prognosis Exceeded) Non-medco GP Medical Report'},
            {type: 'Amendment with Review of Records of Specialist Orthopaedic Medical Report'},
            {type: 'Amendment with Review of Records of Re-examination (Report Rejected) Specialist Orthopaedic Medical Report'},
            {type: 'Amendment with Review of Records of Re-examination(Prognosis Exceeded) Specialist Orthopaedic Medical Report'},
            {type: 'Amendment with Review of Records of Specialist Psychological Medical Report'},
            {type: 'Amendment with Review of Records of Re-examination (Report Rejected) Specialist Psychological Medical Report'},
            {type: 'Amendment with Review of Records of Re-examination (Prognosis Exceeded) Specialist Psychological Medical Report'},
            {type: 'Amendment with Review of Records of Specialist ENT Report'},
            {type: 'Amendment with Review of Records of Specialist Surgeon'},
            {type: 'Amendment with Review of Records of Specialist Dental Report'},
            {type: 'Amendment with Review of Records of Specialist Gynaecology Report'},
            {type: 'Amendment with Review of Records of Specialist Neurology Report'},
            {type: 'Amendment with Review of Records of Holiday Illness Medical Report'},
            {type: 'Amendment with Review of Records of Rehabilitation Physiotherapy Initial Assessment Report'},
            {type: 'Amendment with Review of Records of Rehabilitation Physiotherapy Final Discharge Report'},
            {type: 'Amendment with Review of Records of Other Medical Report (to type)'},
            {type: 'Amendment of MEDCO GP Medical Report with Review of Records'},
            {type: 'Amendment of Re-examination(Report Rejected) MEDCO GP Medical Report with Review of Records'},
            {type: 'Amendment of Re-examination(Prognosis Exceeded) MEDCO GP Medical Report with Review of Records'},
            {type: 'Amendment of Non-medco GP Medical Report with Review of Records'},
            {type: 'Amendment of Re-examination(Report Rejected) Non-medco GP Medical Report with Review of Records'},
            {type: 'Amendment of Re-examination(Prognosis Exceeded) Non-medco GP Medical Report with Review of Records'},
            {type: 'Amendment of Specialist Orthopaedic Medical Report with Review of Records'},
            {type: 'Amendment of Re-examination(Report Rejected) Specialist Orthopaedic Medical Report with Review of Records'},
            {type: 'Amendment of Re-examination(Prognosis Exceeded) Specialist Orthopaedic Medical Report with Review of Records'},
            {type: 'Amendment of Specialist Psychological Medical Report with Review of Records'},
            {type: 'Amendment of Re-examination(Report Rejected) Specialist Psychological Medical Report with Review of Records'},
            {type: 'Amendment of Re-examination(Prognosis Exceeded) Specialist Psychological Medical Report with Review of Records'},
            {type: 'Amendment of Specialist ENT Report with Review of Records'},
            {type: 'Amendment of Specialist Surgeon Report with Review of Records'},
            {type: 'Amendment of Specialist Dental Report with Review of Records'},
            {type: 'Amendment of Specialist Gynaecology Report with Review of Records'},
            {type: 'Amendment of Specialist Neurology Report with Review of Records'},
            {type: 'Amendment of Holiday Illness Medical Report with Review of Records'},
            {type: 'Amendment with Review of Records of MEDCO GP Medical Report with Review of Records'},
            {type: 'Amendment with Review of Records of Re-examination(Report Rejected) MEDCO GP Medical Report with Review of Records'},
            {type: 'Amendment with Review of Records of Re-examination(Prognosis Exceeded) MEDCO GP Medical Report with Review of Records'},
            {type: 'Amendment with Review of Records of Non-medco GP Medical Report with Review of Records'},
            {type: 'Amendment with Review of Records of Re-examination(Report Rejected) Non-medco GP Medical Report with Review of Records'},
            {type: 'Amendment with Review of Records of Re-examination(Prognosis Exceeded) Non-medco GP Medical Report with Review of Records'},
            {type: 'Amendment with Review of Records of Specialist Orthopaedic Medical Report with Review of Records'},
            {type: 'Amendment with Review of Records of Re-examination(Report Rejected) Specialist Orthopaedic Medical Report with Review of Records'},
            {type: 'Amendment with Review of Records of Re-examination(Prognosis Exceeded) Specialist Orthopaedic Medical Report with Review of Records'},
            {type: 'Amendment with Review of Records of Specialist Psychological Medical Report with Review of Records'},
            {type: 'Amendment with Review of Records of Re-examination(Report Rejected) Specialist Psychological Medical Report with Review of Records'},
            {type: 'Amendment with Review of Records of Re-examination(Prognosis Exceeded) Specialist Psychological Medical Report with Review of Records'},
            {type: 'Amendment with Review of Records of Specialist ENT Report with Review of Records'},
            {type: 'Amendment with Review of Records of Specialist Surgeon Report with Review of Records'},
            {type: 'Amendment with Review of Records of Specialist Dental Report with Review of Records'},
            {type: 'Amendment with Review of Records of Specialist Gynaecology Report with Review of Records'},
            {type: 'Amendment with Review of Records of Specialist Neurology Report with Review of Records'},
            {type: 'Amendment with Review of Records of Holiday Illness Medical Report with Review of Records'},
            {type: 'Addendum of MEDCO GP Medical Report'},
            {type: 'Addendum of Re-examination(Report Rejected) MEDCO GP Medical Report'},
            {type: 'Addendum of Re-examination(Prognosis Exceeded) MEDCO GP Medical Report'},
            {type: 'Addendum of Non-medco GP Medical Report'},
            {type: 'Addendum of Re-examination(Report Rejected) Non-medco GP Medical Report'},
            {type: 'Addendum of Re-examination(Prognosis Exceeded) Non-medco GP Medical Report'},
            {type: 'Addendum of Specialist Orthopaedic Medical Report'},
            {type: 'Addendum of Re-examination(Report Rejected) Specialist Orthopaedic Medical Report'},
            {type: 'Addendum of Re-examination(Prognosis Exceeded) Specialist Orthopaedic Medical Report'},
            {type: 'Addendum of Specialist Psychological Medical Report'},
            {type: 'Addendum of Re-examination(Report Rejected) Specialist Psychological Medical Report'},
            {type: 'Addendum of Re-examination(Prognosis Exceeded) Specialist Psychological Medical Report'},
            {type: 'Addendum of Specialist ENT Report'},
            {type: 'Addendum of Specialist Surgeon Report'},
            {type: 'Addendum of Specialist Dental Report'},
            {type: 'Addendum of Specialist Gynaecology Report'},
            {type: 'Addendum of Specialist Neurology Report'},
            {type: 'Addendum of Holiday Illness Medical Report'},
            {type: 'Addendum of Rehabilitation Physiotherapy Initial Assessment Report'},
            {type: 'Addendum of Rehabilitation Physiotherapy Final Discharge Report'},
            {type: 'Addendum of Other Medical Report (to type)'},
            {type: 'Addendum of MEDCO GP Medical Report with Review of Records'},
            {type: 'Addendum of Re-examination(Report Rejected) MEDCO GP Medical Report with Review of Records'},
            {type: 'Addendum of Re-examination(Prognosis Exceeded) MEDCO GP Medical Report with Review of Records'},
            {type: 'Addendum of Non-medco GP Medical Report with Review of Records'},
            {type: 'Addendum of Re-examination(Report Rejected) Non-medco GP Medical Report with Review of Records'},
            {type: 'Addendum of Re-examination(Prognosis Exceeded) Non-medco GP Medical Report with Review of Records'},
            {type: 'Addendum of Specialist Orthopaedic Medical Report with Review of Records'},
            {type: 'Addendum of Re-examination(Report Rejected) Specialist Orthopaedic Medical Report with Review of Records'},
            {type: 'Addendum of Re-examination(Prognosis Exceeded) Specialist Orthopaedic Medical Report with Review of Records'},
            {type: 'Addendum of Specialist Psychological Medical Report with Review of Records'},
            {type: 'Addendum of Re-examination(Report Rejected) Specialist Psychological Medical Report with Review of Records'},
            {type: 'Addendum of Re-examination(Prognosis Exceeded) Specialist Psychological Medical Report with Review of Records'},
            {type: 'Addendum of Specialist ENT Report with Review of Records'},
            {type: 'Addendum of Specialist Surgeon Report with Review of Records'},
            {type: 'Addendum of Specialist Dental Report with Review of Records'},
            {type: 'Addendum of Specialist Gynaecology Report with Review of Records'},
            {type: 'Addendum of Specialist Neurology Report with Review of Records'},
            {type: 'Addendum of Holiday Illness Medical Report with Review of Records'},
            {type: 'Addendum of Rehabilitation Physiotherapy Initial Assessment Report with Review of Records'},
            {type: 'Addendum of Rehabilitation Physiotherapy Final Discharge Report with Review of Records'},
            {type: 'Addendum of Other Medical Report (to type) with Review of Records'},
            {type: 'Addendum of Specialist Plastic Surgeon Report with Review of Records'},
            {type: 'Addendum of Specialist Plastic Surgeon Report'},
            {type: 'Amended of with Review of Records Specialist Plastic Surgeon Report with Review of Records'},
            {type: 'Amended of with Review of Records Specialist Plastic Surgeon Report'},
            {type: 'Part 35 of MEDCO GP Medical Report'},
            {type: 'Part 35 of Re-examination(Report Rejected) MEDCO GP Medical Report'},
            {type: 'Part 35 of Re-examination(Prognosis Exceeded) MEDCO GP Medical Report'},
            {type: 'Part 35 of Non-medco GP Medical Report'},
            {type: 'Part 35 of Re-examination(Report Rejected) Non-medco GP Medical Report'},
            {type: 'Part 35 of Re-examination(Prognosis Exceeded) Non-medco GP Medical Report'},
            {type: 'Part 35 of Specialist Orthopaedic Medical Report'},
            {type: 'Part 35 of Re-examination(Report Rejected) Specialist Orthopaedic Medical Report'},
            {type: 'Part 35 of Re-examination(Prognosis Exceeded) Specialist Orthopaedic Medical Report'},
            {type: 'Part 35 of Specialist Psychological Medical Report'},
            {type: 'Part 35 of Re-examination(Report Rejected) Specialist Psychological Medical Report'},
            {type: 'Part 35 of Re-examination(Prognosis Exceeded) Specialist Psychological Medical Report'},
            {type: 'Part 35 of Specialist ENT Report'},
            {type: 'Part 35 of Specialist Surgeon Report'},
            {type: 'Part 35 of Specialist Dental Report'},
            {type: 'Part 35 of Specialist Gynaecology Report'},
            {type: 'Part 35 of Specialist Neurology Report'},
            {type: 'Part 35 of Holiday Illness Medical Report'},
            {type: 'Part 35 of Other Medical Report (to type)'},
            {type: 'Part 35 of MEDCO GP Medical Report with Review of Records'},
            {type: 'Part 35 of Re-examination(Report Rejected) MEDCO GP Medical Report with Review of Records'},
            {type: 'Part 35 of Re-examination(Prognosis Exceeded) MEDCO GP Medical Report with Review of Records'},
            {type: 'Part 35 of Non-medco GP Medical Report with Review of Records'},
            {type: 'Part 35 of Re-examination(Report Rejected) Non-medco GP Medical Report with Review of Records'},
            {type: 'Part 35 of Re-examination(Prognosis Exceeded) Non-medco GP Medical Report with Review of Records'},
            {type: 'Part 35 of Specialist Orthopaedic Medical Report with Review of Records'},
            {type: 'Part 35 of Re-examination(Report Rejected) Specialist Orthopaedic Medical Report with Review of Records'},
            {type: 'Part 35 of Re-examination(Prognosis Exceeded) Specialist Orthopaedic Medical Report with Review of Records'},
            {type: 'Part 35 of Specialist Psychological Medical Report with Review of Records'},
            {type: 'Part 35 of Re-examination(Report Rejected) Specialist Psychological Medical Report with Review of Records'},
            {type: 'Part 35 of Re-examination(Prognosis Exceeded) Specialist Psychological Medical Report with Review of Records'},
            {type: 'Part 35 of Specialist ENT Report with Review of Records'},
            {type: 'Part 35 of Specialist Surgeon Report with Review of Records'},
            {type: 'Part 35 of Specialist Dental Report with Review of Records'},
            {type: 'Part 35 of Specialist Gynaecology Report with Review of Records'},
            {type: 'Part 35 of Specialist Neurology Report with Review of Records'},
            {type: 'Part 35 of Holiday Illness Medical Report with Review of Records'},
            {type: 'Part 35 of Other Medical Report (to type) with Review of Records'},
            {type: 'Comments of MEDCO GP Medical Report'},
            {type: 'Comments of Re-examination(Report Rejected) MEDCO GP Medical Report'},
            {type: 'Comments of Re-examination(Prognosis Exceeded) MEDCO GP Medical Report'},
            {type: 'Comments of Non-medco GP Medical Report'},
            {type: 'Comments of Re-examination(Report Rejected) Non-medco GP Medical Report'},
            {type: 'Comments of Re-examination(Prognosis Exceeded) Non-medco GP Medical Report'},
            {type: 'Comments of Specialist Orthopaedic Medical Report'},
            {type: 'Comments of Re-examination(Report Rejected) Specialist Orthopaedic Medical Report'},
            {type: 'Comments of Re-examination(Prognosis Exceeded) Specialist Orthopaedic Medical Report'},
            {type: 'Comments of Specialist Psychological Medical Report'},
            {type: 'Comments of Re-examination(Report Rejected) Specialist Psychological Medical Report'},
            {type: 'Comments of Re-examination(Prognosis Exceeded) Specialist Psychological Medical Report'},
            {type: 'Comments of Specialist ENT Report'},
            {type: 'Comments of Specialist Surgeon Report'},
            {type: 'Comments of Specialist Dental Report'},
            {type: 'Comments of Specialist Gynaecology Report'},
            {type: 'Comments of Specialist Neurology Report'},
            {type: 'Comments of Holiday Illness Medical Report'},
            {type: 'Comments of Rehabilitation Physiotherapy Initial Assessment Report'},
            {type: 'Comments of Rehabilitation Physiotherapy Final Discharge Report'},
            {type: 'Comments of Other Medical Report (to type)'},
            {type: 'Comments of MEDCO GP Medical Report with Review of Records'},
            {type: 'Comments of Re-examination(Report Rejected) MEDCO GP Medical Report with Review of Records'},
            {type: 'Comments of Re-examination(Prognosis Exceeded) MEDCO GP Medical Report with Review of Records'},
            {type: 'Comments of Non-medco GP Medical Report with Review of Records'},
            {type: 'Comments of Re-examination(Report Rejected) Non-medco GP Medical Report with Review of Records'},
            {type: 'Comments of Re-examination(Prognosis Exceeded) Non-medco GP Medical Report with Review of Records'},
            {type: 'Comments of Specialist Orthopaedic Medical Report with Review of Records'},
            {type: 'Comments of Re-examination(Report Rejected) Specialist Orthopaedic Medical Report with Review of Records'},
            {type: 'Comments of Re-examination(Prognosis Exceeded) Specialist Orthopaedic Medical Report with Review of Records'},
            {type: 'Comments of Specialist Psychological Medical Report with Review of Records'},
            {type: 'Comments of Re-examination(Report Rejected) Specialist Psychological Medical Report with Review of Records'},
            {type: 'Comments of Re-examination(Prognosis Exceeded) Specialist Psychological Medical Report with Review of Records'},
            {type: 'Comments of Specialist ENT Report with Review of Records'},
            {type: 'Comments of Specialist Surgeon Report with Review of Records'},
            {type: 'Comments of Specialist Dental Report with Review of Records'},
            {type: 'Comments of Specialist Gynaecology Report with Review of Records'},
            {type: 'Comments of Specialist Neurology Report with Review of Records'},
            {type: 'Comments of Other Medical Report (to type) with Review of Records'},
            {type: 'Amendment of Addendum MEDCO GP Medical Report'},
            {type: 'Amendment of Addendum of Re-examination(Report Rejected) MEDCO GP Medical Report'},
            {type: 'Amendment of Addendum of Re-examination(Prognosis Exceeded) MEDCO GP Medical Report'},
            {type: 'Amendment of Addendum Non-medco GP Medical Report'},
            {type: 'Amendment of Addendum of Re-examination(Report Rejected) Non-medco GP Medical Report'},
            {type: 'Amendment of Addendum of Re-examination(Prognosis Exceeded) Non-medco GP Medical Report'},
            {type: 'Amendment of Addendum of Specialist Orthopaedic Medical Report'},
            {type: 'Amendment of Addendum of Re-examination(Report Rejected) Specialist Orthopaedic Medical Report'},
            {type: 'Amendment of Addendum of Re-examination(Prognosis Exceeded) Specialist Orthopaedic Medical Report'},
            {type: 'Amendment of Addendum of Specialist Psychological Medical Report'},
            {type: 'Amendment of Addendum Re-examination(Report Rejected) Specialist Psychological Medical Report'},
            {type: 'Amendment of Addendum Re-examination(Prognosis Exceeded) Specialist Psychological Medical Report'},
            {type: 'Amendment of Addendum of Specialist ENT Report'},
            {type: 'Amendment of Addendum of Specialist Surgeon Report'},
            {type: 'Amendment of Addendum of Specialist Dental Report'},
            {type: 'Amendment of Addendum of Specialist Gynaecology Report'},
            {type: 'Amendment of Addendum of Specialist Neurology Report'},
            {type: 'Amendment of Addendum of Holiday Illness Medical Report'},
            {type: 'Amendment of Addendum of Rehabilitation Physiotherapy Initial Assessment Report'},
            {type: 'Amendment of Addendum of Rehabilitation Physiotherapy Final Discharge Report'},
            {type: 'Amendment of Addendum of Other Medical Report (to type)'},
            {type: 'Amendment of Addendum MEDCO GP Medical Report with Review of Records'},
            {type: 'Amendment of Addendum of Re-examination(Report Rejected) MEDCO GP Medical Report with Review of Records'},
            {type: 'Amendment of Addendum of Re-examination(Prognosis Exceeded) MEDCO GP Medical Report with Review of Records'},
            {type: 'Amendment of Addendum Non-medco GP Medical Report with Review of Records'},
            {type: 'Amendment of Addendum of Re-examination(Report Rejected) Non-medco GP Medical Report with Review of Records'},
            {type: 'Amendment of Addendum of Re-examination(Prognosis Exceeded) Non-medco GP Medical Report with Review of Records'},
            {type: 'Amendment of Addendum of Specialist Orthopaedic Medical Report with Review of Records'},
            {type: 'Amendment of Addendum of Re-examination(Report Rejected) Specialist Orthopaedic Medical Report with Review of Records'},
            {type: 'Amendment of Addendum of Re-examination(Prognosis Exceeded) Specialist Orthopaedic Medical Report with Review of Records'},
            {type: 'Amendment of Addendum of Specialist Psychological Medical Report with Review of Records'},
            {type: 'Amendment of Addendum Re-examination(Report Rejected) Specialist Psychological Medical Report with Review of Records'},
            {type: 'Amendment of Addendum Re-examination(Prognosis Exceeded) Specialist Psychological Medical Report with Review of Records'},
            {type: 'Amendment of Addendum of Specialist ENT Report with Review of Records'},
            {type: 'Amendment of Addendum of Specialist Surgeon Report with Review of Records'},
            {type: 'Amendment of Addendum of Specialist Dental Report with Review of Records'},
            {type: 'Amendment of Addendum of Specialist Gynaecology Report with Review of Records'},
            {type: 'Amendment of Addendum of Specialist Neurology Report with Review of Records'},
            {type: 'Amendment of Addendum of Holiday Illness Medical Report with Review of Records'},
            {type: 'Amendment of Part 35 of MEDCO GP Medical Report'},
            {type: 'Amendment of Part 35 of Re-examination(Report Rejected) MEDCO GP Medical Report'},
            {type: 'Amendment of Part 35 of Re-examination(Prognosis Exceeded) MEDCO GP Medical Report'},
            {type: 'Amendment of Part 35 of Non-medco GP Medical Report'},
            {type: 'Amendment of Part 35 of  Re-examination(Report Rejected) Non-medco GP Medical Report'},
            {type: 'Amendment of Part 35 of  Re-examination(Prognosis Exceeded) Non-medco GP Medical Report'},
            {type: 'Amendment of Part 35 of  Specialist Orthopaedic Medical Report'},
            {type: 'Amendment of Part 35 of Re-examination(Report Rejected) Specialist Orthopaedic Medical Report'},
            {type: 'Amendment of Part 35 of Re-examination(Prognosis Exceeded) Specialist Orthopaedic Medical Report'},
            {type: 'Amendment of Part 35 of  Specialist Psychological Medical Report'},
            {type: 'Amendment of Part 35 of Re-examination(Report Rejected) Specialist Psychological Medical Report'},
            {type: 'Amendment of Part 35 of Re-examination(Prognosis Exceeded) Specialist Psychological Medical Report'},
            {type: 'Amendment of Part 35 of  Specialist ENT Report'},
            {type: 'Amendment of Part 35 of Specialist Surgeon Report'},
            {type: 'Amendment of Part 35 of Specialist Dental Report'},
            {type: 'Amendment of Part 35 of Specialist Gynaecology Report'},
            {type: 'Amendment of Part 35 of  Specialist Neurology Report'},
            {type: 'Amendment of Part 35 of Holiday Illness Medical Report'},
            {type: 'Amendment of Part 35 of Other Medical Report (to type)'},
            {type: 'Amendment of Part 35 of MEDCO GP Medical Report with Review of Records'},
            {type: 'Amendment of Part 35 of Re-examination(Report Rejected) MEDCO GP Medical Report with Review of Records'},
            {type: 'Amendment of Part 35 of Re-examination(Prognosis Exceeded) MEDCO GP Medical Report with Review of Records'},
            {type: 'Amendment of Part 35 of Non-medco GP Medical Report with Review of Records'},
            {type: 'Amendment of Part 35 of  Re-examination(Report Rejected) Non-medco GP Medical Report with Review of Records'},
            {type: 'Amendment of Part 35 of  Re-examination(Prognosis Exceeded) Non-medco GP Medical Report with Review of Records'},
            {type: 'Amendment of Part 35 of  Specialist Orthopaedic Medical Report with Review of Records'},
            {type: 'Amendment of Part 35 of Re-examination(Report Rejected) Specialist Orthopaedic Medical Report with Review of Records'},
            {type: 'Amendment of Part 35 of Re-examination(Prognosis Exceeded) Specialist Orthopaedic Medical Report with Review of Records'},
            {type: 'Amendment of Part 35 of  Specialist Psychological Medical Report with Review of Records'},
            {type: 'Amendment of Part 35 of Re-examination(Report Rejected) Specialist Psychological Medical Report with Review of Records'},
            {type: 'Amendment of Part 35 of Re-examination(Prognosis Exceeded) Specialist Psychological Medical Report with Review of Records'},
            {type: 'Amendment of Part 35 of  Specialist ENT Report with Review of Records'},
            {type: 'Amendment of Part 35 of Specialist Surgeon Report with Review of Records'},
            {type: 'Amendment of Part 35 of Specialist Dental Report with Review of Records'},
            {type: 'Amendment of Part 35 of Specialist Gynaecology Report with Review of Records'},
            {type: 'Amendment of Part 35 of  Specialist Neurology Report with Review of Records'},
            {type: 'Amendment of Part 35 of Holiday Illness Medical Report with Review of Records'},
            {type: 'Amendment of Part 35 of Other Medical Report (to type) with Review of Records'},
            {type: 'Amendment of Supplementary MEDCO GP Medical Report'},
            {type: 'Amendment of Supplementary Re-examination(Report Rejected) MEDCO GP Medical Report'},
            {type: 'Amendment of Supplementary Re-examination(Prognosis Exceeded) MEDCO GP Medical Report'},
            {type: 'Amendment of Supplementary Non-medco GP Medical Report'},
            {type: 'Amendment of Supplementary Re-examination(Report Rejected) Non-medco GP Medical Report'},
            {type: 'Amendment of Supplementary Re-examination(Prognosis Exceeded) Non-medco GP Medical Report'},
            {type: 'Amendment of Supplementary Specialist Orthopaedic Medical Report'},
            {type: 'Amendment of Supplementary Re-examination(Report Rejected) Specialist Orthopaedic Medical Report'},
            {type: 'Amendment of Supplementary Re-examination(Prognosis Exceeded) Specialist Orthopaedic Medical Report'},
            {type: 'Amendment of Supplementary Specialist Psychological Medical Report'},
            {type: 'Amendment of Supplementary Re-examination(Report Rejected) Specialist Psychological Medical Report'},
            {type: 'Amendment of Supplementary Re-examination (Prognosis Exceeded) Specialist Psychological Medical Report'},
            {type: 'Amendment of Supplementary Specialist ENT Report'},
            {type: 'Amendment of Supplementary Specialist Surgeon Report'},
            {type: 'Amendment of Supplementary Specialist Dental Report'},
            {type: 'Amendment of Supplementary Specialist Gynaecology Report'},
            {type: 'Amendment of Supplementary Specialist Neurology Report'},
            {type: 'Amendment of Supplementary Holiday Illness Medical Report'},
            {type: 'Amendment of Supplementary Other Medical Report (to type)Request for Amendment of Supplementary MEDCO GP Medical Report with Review of Records'},
            {type: 'Amendment of Supplementary Re-examination(Report Rejected) MEDCO GP Medical Report with Review of Records'},
            {type: 'Amendment of Supplementary Re-examination(Prognosis Exceeded) MEDCO GP Medical Report with Review of Records'},
            {type: 'Amendment of Supplementary Non-medco GP Medical Report with Review of Records'},
            {type: 'Amendment of Supplementary Re-examination(Report Rejected) Non-medco GP Medical Report with Review of Records'},
            {type: 'Amendment of Supplementary Re-examination(Prognosis Exceeded) Non-medco GP Medical Report with Review of Records'},
            {type: 'Amendment of Supplementary Specialist Orthopaedic Medical Report with Review of Records'},
            {type: 'Amendment of Supplementary Re-examination(Report Rejected) Specialist Orthopaedic Medical Report with Review of Records'},
            {type: 'Amendment of Supplementary Re-examination(Prognosis Exceeded) Specialist Orthopaedic Medical Report with Review of Records'},
            {type: 'Amendment of Supplementary Specialist Psychological Medical Report with Review of Records'},
            {type: 'Amendment of Supplementary Re-examination(Report Rejected) Specialist Psychological Medical Report with Review of Records'},
            {type: 'Amendment of Supplementary Re-examination (Prognosis Exceeded) Specialist Psychological Medical Report with Review of Records'},
            {type: 'Amendment of Supplementary Specialist ENT Report with Review of Records'},
            {type: 'Amendment of Supplementary Specialist Surgeon Report with Review of Records'},
            {type: 'Amendment of Supplementary Specialist Dental Report with Review of Records'},
            {type: 'Amendment of Supplementary Specialist Gynaecology Report with Review of Records'},
            {type: 'Amendment of Supplementary Specialist Neurology Report with Review of Records'},
            {type: 'Amendment of Supplementary Holiday Illness Medical Report with Review of Records'},
            {type: 'Amendment of Supplementary Other Medical Report (to type)'},
        ],
        request_types: [
            {type: 'Amendment of MEDCO GP Medical Report'},
            {type: 'Amendment of Re-examination(Report Rejected) MEDCO GP Medical Report'},
            {type: 'Amendment of Re-examination(Prognosis Exceeded) MEDCO GP Medical Report'},
            {type: 'Amendment of Non-medco GP Medical Report'},
            {type: 'Amendment of Re-examination (Report Rejected) Non-medco GP Medical Report'},
            {type: 'Amendment of Re-examination (Prognosis Exceeded) Non-medco GP Medical Report'},
            {type: 'Amendment of Specialist Orthopaedic Medical Report'},
            {type: 'Amendment of Re-examination (Report Rejected) Specialist Orthopaedic Medical Report'},
            {type: 'Amendment of Re-examination(Prognosis Exceeded) Specialist Orthopaedic Medical Report'},
            {type: 'Amendment of Specialist Psychological Medical Report'},
            {type: 'Amendment of Re-examination (Report Rejected) Specialist Psychological Medical Report'},
            {type: 'Amendment of Re-examination (Prognosis Exceeded) Specialist Psychological Medical Report'},
            {type: 'Amendment of Specialist ENT Report'},
            {type: 'Amendment of Specialist Surgeon'},
            {type: 'Amendment of Specialist Dental Report'},
            {type: 'Amendment of Specialist Gynaecology Report'},
            {type: 'Amendment of Specialist Neurology Report'},
            {type: 'Amendment of Holiday Illness Medical Report'},
            {type: 'Amendment of Rehabilitation Physiotherapy Initial Assessment Report'},
            {type: 'Amendment of Rehabilitation Physiotherapy Final Discharge Report'},
            {type: 'Amendment of Other Medical Report (to type)'},
            {type: 'Amendment with Review of Records of MEDCO GP Medical Report'},
            {type: 'Amendment with Review of Records of Re-examination(Report Rejected) MEDCO GP Medical Report'},
            {type: 'Amendment with Review of Records of Re-examination(Prognosis Exceeded) MEDCO GP Medical Report'},
            {type: 'Amendment with Review of Records of Non-medco GP Medical Report'},
            {type: 'Amendment with Review of Records of Re-examination (Report Rejected) Non-medco GP Medical Report'},
            {type: 'Amendment with Review of Records of Re-examination (Prognosis Exceeded) Non-medco GP Medical Report'},
            {type: 'Amendment with Review of Records of Specialist Orthopaedic Medical Report'},
            {type: 'Amendment with Review of Records of Re-examination (Report Rejected) Specialist Orthopaedic Medical Report'},
            {type: 'Amendment with Review of Records of Re-examination(Prognosis Exceeded) Specialist Orthopaedic Medical Report'},
            {type: 'Amendment with Review of Records of Specialist Psychological Medical Report'},
            {type: 'Amendment with Review of Records of Re-examination (Report Rejected) Specialist Psychological Medical Report'},
            {type: 'Amendment with Review of Records of Re-examination (Prognosis Exceeded) Specialist Psychological Medical Report'},
            {type: 'Amendment with Review of Records of Specialist ENT Report'},
            {type: 'Amendment with Review of Records of Specialist Surgeon'},
            {type: 'Amendment with Review of Records of Specialist Dental Report'},
            {type: 'Amendment with Review of Records of Specialist Gynaecology Report'},
            {type: 'Amendment with Review of Records of Specialist Neurology Report'},
            {type: 'Amendment with Review of Records of Holiday Illness Medical Report'},
            {type: 'Amendment with Review of Records of Rehabilitation Physiotherapy Initial Assessment Report'},
            {type: 'Amendment with Review of Records of Rehabilitation Physiotherapy Final Discharge Report'},
            {type: 'Amendment with Review of Records of Other Medical Report (to type)'},
            {type: 'Amendment of MEDCO GP Medical Report with Review of Records'},
            {type: 'Amendment of Re-examination(Report Rejected) MEDCO GP Medical Report with Review of Records'},
            {type: 'Amendment of Re-examination(Prognosis Exceeded) MEDCO GP Medical Report with Review of Records'},
            {type: 'Amendment of Non-medco GP Medical Report with Review of Records'},
            {type: 'Amendment of Re-examination(Report Rejected) Non-medco GP Medical Report with Review of Records'},
            {type: 'Amendment of Re-examination(Prognosis Exceeded) Non-medco GP Medical Report with Review of Records'},
            {type: 'Amendment of Specialist Orthopaedic Medical Report with Review of Records'},
            {type: 'Amendment of Re-examination(Report Rejected) Specialist Orthopaedic Medical Report with Review of Records'},
            {type: 'Amendment of Re-examination(Prognosis Exceeded) Specialist Orthopaedic Medical Report with Review of Records'},
            {type: 'Amendment of Specialist Psychological Medical Report with Review of Records'},
            {type: 'Amendment of Re-examination(Report Rejected) Specialist Psychological Medical Report with Review of Records'},
            {type: 'Amendment of Re-examination(Prognosis Exceeded) Specialist Psychological Medical Report with Review of Records'},
            {type: 'Amendment of Specialist ENT Report with Review of Records'},
            {type: 'Amendment of Specialist Surgeon Report with Review of Records'},
            {type: 'Amendment of Specialist Dental Report with Review of Records'},
            {type: 'Amendment of Specialist Gynaecology Report with Review of Records'},
            {type: 'Amendment of Specialist Neurology Report with Review of Records'},
            {type: 'Amendment of Holiday Illness Medical Report with Review of Records'},
            {type: 'Amendment with Review of Records of MEDCO GP Medical Report with Review of Records'},
            {type: 'Amendment with Review of Records of Re-examination(Report Rejected) MEDCO GP Medical Report with Review of Records'},
            {type: 'Amendment with Review of Records of Re-examination(Prognosis Exceeded) MEDCO GP Medical Report with Review of Records'},
            {type: 'Amendment with Review of Records of Non-medco GP Medical Report with Review of Records'},
            {type: 'Amendment with Review of Records of Re-examination(Report Rejected) Non-medco GP Medical Report with Review of Records'},
            {type: 'Amendment with Review of Records of Re-examination(Prognosis Exceeded) Non-medco GP Medical Report with Review of Records'},
            {type: 'Amendment with Review of Records of Specialist Orthopaedic Medical Report with Review of Records'},
            {type: 'Amendment with Review of Records of Re-examination(Report Rejected) Specialist Orthopaedic Medical Report with Review of Records'},
            {type: 'Amendment with Review of Records of Re-examination(Prognosis Exceeded) Specialist Orthopaedic Medical Report with Review of Records'},
            {type: 'Amendment with Review of Records of Specialist Psychological Medical Report with Review of Records'},
            {type: 'Amendment with Review of Records of Re-examination(Report Rejected) Specialist Psychological Medical Report with Review of Records'},
            {type: 'Amendment with Review of Records of Re-examination(Prognosis Exceeded) Specialist Psychological Medical Report with Review of Records'},
            {type: 'Amendment with Review of Records of Specialist ENT Report with Review of Records'},
            {type: 'Amendment with Review of Records of Specialist Surgeon Report with Review of Records'},
            {type: 'Amendment with Review of Records of Specialist Dental Report with Review of Records'},
            {type: 'Amendment with Review of Records of Specialist Gynaecology Report with Review of Records'},
            {type: 'Amendment with Review of Records of Specialist Neurology Report with Review of Records'},
            {type: 'Amendment with Review of Records of Holiday Illness Medical Report with Review of Records'},
            {type: 'Addendum of MEDCO GP Medical Report'},
            {type: 'Addendum of Re-examination(Report Rejected) MEDCO GP Medical Report'},
            {type: 'Addendum of Re-examination(Prognosis Exceeded) MEDCO GP Medical Report'},
            {type: 'Addendum of Non-medco GP Medical Report'},
            {type: 'Addendum of Re-examination(Report Rejected) Non-medco GP Medical Report'},
            {type: 'Addendum of Re-examination(Prognosis Exceeded) Non-medco GP Medical Report'},
            {type: 'Addendum of Specialist Orthopaedic Medical Report'},
            {type: 'Addendum of Re-examination(Report Rejected) Specialist Orthopaedic Medical Report'},
            {type: 'Addendum of Re-examination(Prognosis Exceeded) Specialist Orthopaedic Medical Report'},
            {type: 'Addendum of Specialist Psychological Medical Report'},
            {type: 'Addendum of Re-examination(Report Rejected) Specialist Psychological Medical Report'},
            {type: 'Addendum of Re-examination(Prognosis Exceeded) Specialist Psychological Medical Report'},
            {type: 'Addendum of Specialist ENT Report'},
            {type: 'Addendum of Specialist Surgeon Report'},
            {type: 'Addendum of Specialist Dental Report'},
            {type: 'Addendum of Specialist Gynaecology Report'},
            {type: 'Addendum of Specialist Neurology Report'},
            {type: 'Addendum of Holiday Illness Medical Report'},
            {type: 'Addendum of Rehabilitation Physiotherapy Initial Assessment Report'},
            {type: 'Addendum of Rehabilitation Physiotherapy Final Discharge Report'},
            {type: 'Addendum of Other Medical Report (to type)'},
            {type: 'Addendum of MEDCO GP Medical Report with Review of Records'},
            {type: 'Addendum of Re-examination(Report Rejected) MEDCO GP Medical Report with Review of Records'},
            {type: 'Addendum of Re-examination(Prognosis Exceeded) MEDCO GP Medical Report with Review of Records'},
            {type: 'Addendum of Non-medco GP Medical Report with Review of Records'},
            {type: 'Addendum of Re-examination(Report Rejected) Non-medco GP Medical Report with Review of Records'},
            {type: 'Addendum of Re-examination(Prognosis Exceeded) Non-medco GP Medical Report with Review of Records'},
            {type: 'Addendum of Specialist Orthopaedic Medical Report with Review of Records'},
            {type: 'Addendum of Re-examination(Report Rejected) Specialist Orthopaedic Medical Report with Review of Records'},
            {type: 'Addendum of Re-examination(Prognosis Exceeded) Specialist Orthopaedic Medical Report with Review of Records'},
            {type: 'Addendum of Specialist Psychological Medical Report with Review of Records'},
            {type: 'Addendum of Re-examination(Report Rejected) Specialist Psychological Medical Report with Review of Records'},
            {type: 'Addendum of Re-examination(Prognosis Exceeded) Specialist Psychological Medical Report with Review of Records'},
            {type: 'Addendum of Specialist ENT Report with Review of Records'},
            {type: 'Addendum of Specialist Surgeon Report with Review of Records'},
            {type: 'Addendum of Specialist Dental Report with Review of Records'},
            {type: 'Addendum of Specialist Gynaecology Report with Review of Records'},
            {type: 'Addendum of Specialist Neurology Report with Review of Records'},
            {type: 'Addendum of Holiday Illness Medical Report with Review of Records'},
            {type: 'Addendum of Rehabilitation Physiotherapy Initial Assessment Report with Review of Records'},
            {type: 'Addendum of Rehabilitation Physiotherapy Final Discharge Report with Review of Records'},
            {type: 'Addendum of Other Medical Report (to type) with Review of Records'},
            {type: 'Part 35 of MEDCO GP Medical Report'},
            {type: 'Part 35 of Re-examination(Report Rejected) MEDCO GP Medical Report'},
            {type: 'Part 35 of Re-examination(Prognosis Exceeded) MEDCO GP Medical Report'},
            {type: 'Part 35 of Non-medco GP Medical Report'},
            {type: 'Part 35 of Re-examination(Report Rejected) Non-medco GP Medical Report'},
            {type: 'Part 35 of Re-examination(Prognosis Exceeded) Non-medco GP Medical Report'},
            {type: 'Part 35 of Specialist Orthopaedic Medical Report'},
            {type: 'Part 35 of Re-examination(Report Rejected) Specialist Orthopaedic Medical Report'},
            {type: 'Part 35 of Re-examination(Prognosis Exceeded) Specialist Orthopaedic Medical Report'},
            {type: 'Part 35 of Specialist Psychological Medical Report'},
            {type: 'Part 35 of Re-examination(Report Rejected) Specialist Psychological Medical Report'},
            {type: 'Part 35 of Re-examination(Prognosis Exceeded) Specialist Psychological Medical Report'},
            {type: 'Part 35 of Specialist ENT Report'},
            {type: 'Part 35 of Specialist Surgeon Report'},
            {type: 'Part 35 of Specialist Dental Report'},
            {type: 'Part 35 of Specialist Gynaecology Report'},
            {type: 'Part 35 of Specialist Neurology Report'},
            {type: 'Part 35 of Holiday Illness Medical Report'},
            {type: 'Part 35 of Other Medical Report (to type)'},
            {type: 'Part 35 of MEDCO GP Medical Report with Review of Records'},
            {type: 'Part 35 of Re-examination(Report Rejected) MEDCO GP Medical Report with Review of Records'},
            {type: 'Part 35 of Re-examination(Prognosis Exceeded) MEDCO GP Medical Report with Review of Records'},
            {type: 'Part 35 of Non-medco GP Medical Report with Review of Records'},
            {type: 'Part 35 of Re-examination(Report Rejected) Non-medco GP Medical Report with Review of Records'},
            {type: 'Part 35 of Re-examination(Prognosis Exceeded) Non-medco GP Medical Report with Review of Records'},
            {type: 'Part 35 of Specialist Orthopaedic Medical Report with Review of Records'},
            {type: 'Part 35 of Re-examination(Report Rejected) Specialist Orthopaedic Medical Report with Review of Records'},
            {type: 'Part 35 of Re-examination(Prognosis Exceeded) Specialist Orthopaedic Medical Report with Review of Records'},
            {type: 'Part 35 of Specialist Psychological Medical Report with Review of Records'},
            {type: 'Part 35 of Re-examination(Report Rejected) Specialist Psychological Medical Report with Review of Records'},
            {type: 'Part 35 of Re-examination(Prognosis Exceeded) Specialist Psychological Medical Report with Review of Records'},
            {type: 'Part 35 of Specialist ENT Report with Review of Records'},
            {type: 'Part 35 of Specialist Surgeon Report with Review of Records'},
            {type: 'Part 35 of Specialist Dental Report with Review of Records'},
            {type: 'Part 35 of Specialist Gynaecology Report with Review of Records'},
            {type: 'Part 35 of Specialist Neurology Report with Review of Records'},
            {type: 'Part 35 of Holiday Illness Medical Report with Review of Records'},
            {type: 'Part 35 of Other Medical Report (to type) with Review of Records'},
            {type: 'Comments of MEDCO GP Medical Report'},
            {type: 'Comments of Re-examination(Report Rejected) MEDCO GP Medical Report'},
            {type: 'Comments of Re-examination(Prognosis Exceeded) MEDCO GP Medical Report'},
            {type: 'Comments of Non-medco GP Medical Report'},
            {type: 'Comments of Re-examination(Report Rejected) Non-medco GP Medical Report'},
            {type: 'Comments of Re-examination(Prognosis Exceeded) Non-medco GP Medical Report'},
            {type: 'Comments of Specialist Orthopaedic Medical Report'},
            {type: 'Comments of Re-examination(Report Rejected) Specialist Orthopaedic Medical Report'},
            {type: 'Comments of Re-examination(Prognosis Exceeded) Specialist Orthopaedic Medical Report'},
            {type: 'Comments of Specialist Psychological Medical Report'},
            {type: 'Comments of Re-examination(Report Rejected) Specialist Psychological Medical Report'},
            {type: 'Comments of Re-examination(Prognosis Exceeded) Specialist Psychological Medical Report'},
            {type: 'Comments of Specialist ENT Report'},
            {type: 'Comments of Specialist Surgeon Report'},
            {type: 'Comments of Specialist Dental Report'},
            {type: 'Comments of Specialist Gynaecology Report'},
            {type: 'Comments of Specialist Neurology Report'},
            {type: 'Comments of Holiday Illness Medical Report'},
            {type: 'Comments of Rehabilitation Physiotherapy Initial Assessment Report'},
            {type: 'Comments of Rehabilitation Physiotherapy Final Discharge Report'},
            {type: 'Comments of Other Medical Report (to type)'},
            {type: 'Comments of MEDCO GP Medical Report with Review of Records'},
            {type: 'Comments of Re-examination(Report Rejected) MEDCO GP Medical Report with Review of Records'},
            {type: 'Comments of Re-examination(Prognosis Exceeded) MEDCO GP Medical Report with Review of Records'},
            {type: 'Comments of Non-medco GP Medical Report with Review of Records'},
            {type: 'Comments of Re-examination(Report Rejected) Non-medco GP Medical Report with Review of Records'},
            {type: 'Comments of Re-examination(Prognosis Exceeded) Non-medco GP Medical Report with Review of Records'},
            {type: 'Comments of Specialist Orthopaedic Medical Report with Review of Records'},
            {type: 'Comments of Re-examination(Report Rejected) Specialist Orthopaedic Medical Report with Review of Records'},
            {type: 'Comments of Re-examination(Prognosis Exceeded) Specialist Orthopaedic Medical Report with Review of Records'},
            {type: 'Comments of Specialist Psychological Medical Report with Review of Records'},
            {type: 'Comments of Re-examination(Report Rejected) Specialist Psychological Medical Report with Review of Records'},
            {type: 'Comments of Re-examination(Prognosis Exceeded) Specialist Psychological Medical Report with Review of Records'},
            {type: 'Comments of Specialist ENT Report with Review of Records'},
            {type: 'Comments of Specialist Surgeon Report with Review of Records'},
            {type: 'Comments of Specialist Dental Report with Review of Records'},
            {type: 'Comments of Specialist Gynaecology Report with Review of Records'},
            {type: 'Comments of Specialist Neurology Report with Review of Records'},
            {type: 'Comments of Other Medical Report (to type) with Review of Records'},
            {type: 'Amendment of Addendum MEDCO GP Medical Report'},
            {type: 'Amendment of Addendum of Re-examination(Report Rejected) MEDCO GP Medical Report'},
            {type: 'Amendment of Addendum of Re-examination(Prognosis Exceeded) MEDCO GP Medical Report'},
            {type: 'Amendment of Addendum Non-medco GP Medical Report'},
            {type: 'Amendment of Addendum of Re-examination(Report Rejected) Non-medco GP Medical Report'},
            {type: 'Amendment of Addendum of Re-examination(Prognosis Exceeded) Non-medco GP Medical Report'},
            {type: 'Amendment of Addendum of Specialist Orthopaedic Medical Report'},
            {type: 'Amendment of Addendum of Re-examination(Report Rejected) Specialist Orthopaedic Medical Report'},
            {type: 'Amendment of Addendum of Re-examination(Prognosis Exceeded) Specialist Orthopaedic Medical Report'},
            {type: 'Amendment of Addendum of Specialist Psychological Medical Report'},
            {type: 'Amendment of Addendum Re-examination(Report Rejected) Specialist Psychological Medical Report'},
            {type: 'Amendment of Addendum Re-examination(Prognosis Exceeded) Specialist Psychological Medical Report'},
            {type: 'Amendment of Addendum of Specialist ENT Report'},
            {type: 'Amendment of Addendum of Specialist Surgeon Report'},
            {type: 'Amendment of Addendum of Specialist Dental Report'},
            {type: 'Amendment of Addendum of Specialist Gynaecology Report'},
            {type: 'Amendment of Addendum of Specialist Neurology Report'},
            {type: 'Amendment of Addendum of Holiday Illness Medical Report'},
            {type: 'Amendment of Addendum of Rehabilitation Physiotherapy Initial Assessment Report'},
            {type: 'Amendment of Addendum of Rehabilitation Physiotherapy Final Discharge Report'},
            {type: 'Amendment of Addendum of Other Medical Report (to type)'},
            {type: 'Amendment of Addendum MEDCO GP Medical Report with Review of Records'},
            {type: 'Amendment of Addendum of Re-examination(Report Rejected) MEDCO GP Medical Report with Review of Records'},
            {type: 'Amendment of Addendum of Re-examination(Prognosis Exceeded) MEDCO GP Medical Report with Review of Records'},
            {type: 'Amendment of Addendum Non-medco GP Medical Report with Review of Records'},
            {type: 'Amendment of Addendum of Re-examination(Report Rejected) Non-medco GP Medical Report with Review of Records'},
            {type: 'Amendment of Addendum of Re-examination(Prognosis Exceeded) Non-medco GP Medical Report with Review of Records'},
            {type: 'Amendment of Addendum of Specialist Orthopaedic Medical Report with Review of Records'},
            {type: 'Amendment of Addendum of Re-examination(Report Rejected) Specialist Orthopaedic Medical Report with Review of Records'},
            {type: 'Amendment of Addendum of Re-examination(Prognosis Exceeded) Specialist Orthopaedic Medical Report with Review of Records'},
            {type: 'Amendment of Addendum of Specialist Psychological Medical Report with Review of Records'},
            {type: 'Amendment of Addendum Re-examination(Report Rejected) Specialist Psychological Medical Report with Review of Records'},
            {type: 'Amendment of Addendum Re-examination(Prognosis Exceeded) Specialist Psychological Medical Report with Review of Records'},
            {type: 'Amendment of Addendum of Specialist ENT Report with Review of Records'},
            {type: 'Amendment of Addendum of Specialist Surgeon Report with Review of Records'},
            {type: 'Amendment of Addendum of Specialist Dental Report with Review of Records'},
            {type: 'Amendment of Addendum of Specialist Gynaecology Report with Review of Records'},
            {type: 'Amendment of Addendum of Specialist Neurology Report with Review of Records'},
            {type: 'Amendment of Addendum of Holiday Illness Medical Report with Review of Records'},
            {type: 'Amendment of Part 35 of MEDCO GP Medical Report'},
            {type: 'Amendment of Part 35 of Re-examination(Report Rejected) MEDCO GP Medical Report'},
            {type: 'Amendment of Part 35 of Re-examination(Prognosis Exceeded) MEDCO GP Medical Report'},
            {type: 'Amendment of Part 35 of Non-medco GP Medical Report'},
            {type: 'Amendment of Part 35 of  Re-examination(Report Rejected) Non-medco GP Medical Report'},
            {type: 'Amendment of Part 35 of  Re-examination(Prognosis Exceeded) Non-medco GP Medical Report'},
            {type: 'Amendment of Part 35 of  Specialist Orthopaedic Medical Report'},
            {type: 'Amendment of Part 35 of Re-examination(Report Rejected) Specialist Orthopaedic Medical Report'},
            {type: 'Amendment of Part 35 of Re-examination(Prognosis Exceeded) Specialist Orthopaedic Medical Report'},
            {type: 'Amendment of Part 35 of  Specialist Psychological Medical Report'},
            {type: 'Amendment of Part 35 of Re-examination(Report Rejected) Specialist Psychological Medical Report'},
            {type: 'Amendment of Part 35 of Re-examination(Prognosis Exceeded) Specialist Psychological Medical Report'},
            {type: 'Amendment of Part 35 of  Specialist ENT Report'},
            {type: 'Amendment of Part 35 of Specialist Surgeon Report'},
            {type: 'Amendment of Part 35 of Specialist Dental Report'},
            {type: 'Amendment of Part 35 of Specialist Gynaecology Report'},
            {type: 'Amendment of Part 35 of  Specialist Neurology Report'},
            {type: 'Amendment of Part 35 of Holiday Illness Medical Report'},
            {type: 'Amendment of Part 35 of Other Medical Report (to type)'},
            {type: 'Amendment of Part 35 of MEDCO GP Medical Report with Review of Records'},
            {type: 'Amendment of Part 35 of Re-examination(Report Rejected) MEDCO GP Medical Report with Review of Records'},
            {type: 'Amendment of Part 35 of Re-examination(Prognosis Exceeded) MEDCO GP Medical Report with Review of Records'},
            {type: 'Amendment of Part 35 of Non-medco GP Medical Report with Review of Records'},
            {type: 'Amendment of Part 35 of  Re-examination(Report Rejected) Non-medco GP Medical Report with Review of Records'},
            {type: 'Amendment of Part 35 of  Re-examination(Prognosis Exceeded) Non-medco GP Medical Report with Review of Records'},
            {type: 'Amendment of Part 35 of  Specialist Orthopaedic Medical Report with Review of Records'},
            {type: 'Amendment of Part 35 of Re-examination(Report Rejected) Specialist Orthopaedic Medical Report with Review of Records'},
            {type: 'Amendment of Part 35 of Re-examination(Prognosis Exceeded) Specialist Orthopaedic Medical Report with Review of Records'},
            {type: 'Amendment of Part 35 of  Specialist Psychological Medical Report with Review of Records'},
            {type: 'Amendment of Part 35 of Re-examination(Report Rejected) Specialist Psychological Medical Report with Review of Records'},
            {type: 'Amendment of Part 35 of Re-examination(Prognosis Exceeded) Specialist Psychological Medical Report with Review of Records'},
            {type: 'Amendment of Part 35 of  Specialist ENT Report with Review of Records'},
            {type: 'Amendment of Part 35 of Specialist Surgeon Report with Review of Records'},
            {type: 'Amendment of Part 35 of Specialist Dental Report with Review of Records'},
            {type: 'Amendment of Part 35 of Specialist Gynaecology Report with Review of Records'},
            {type: 'Amendment of Part 35 of  Specialist Neurology Report with Review of Records'},
            {type: 'Amendment of Part 35 of Holiday Illness Medical Report with Review of Records'},
            {type: 'Amendment of Part 35 of Other Medical Report (to type) with Review of Records'},
            {type: 'Amendment of Supplementary MEDCO GP Medical Report'},
            {type: 'Amendment of Supplementary Re-examination(Report Rejected) MEDCO GP Medical Report'},
            {type: 'Amendment of Supplementary Re-examination(Prognosis Exceeded) MEDCO GP Medical Report'},
            {type: 'Amendment of Supplementary Non-medco GP Medical Report'},
            {type: 'Amendment of Supplementary Re-examination(Report Rejected) Non-medco GP Medical Report'},
            {type: 'Amendment of Supplementary Re-examination(Prognosis Exceeded) Non-medco GP Medical Report'},
            {type: 'Amendment of Supplementary Specialist Orthopaedic Medical Report'},
            {type: 'Amendment of Supplementary Re-examination(Report Rejected) Specialist Orthopaedic Medical Report'},
            {type: 'Amendment of Supplementary Re-examination(Prognosis Exceeded) Specialist Orthopaedic Medical Report'},
            {type: 'Amendment of Supplementary Specialist Psychological Medical Report'},
            {type: 'Amendment of Supplementary Re-examination(Report Rejected) Specialist Psychological Medical Report'},
            {type: 'Amendment of Supplementary Re-examination (Prognosis Exceeded) Specialist Psychological Medical Report'},
            {type: 'Amendment of Supplementary Specialist ENT Report'},
            {type: 'Amendment of Supplementary Specialist Surgeon Report'},
            {type: 'Amendment of Supplementary Specialist Dental Report'},
            {type: 'Amendment of Supplementary Specialist Gynaecology Report'},
            {type: 'Amendment of Supplementary Specialist Neurology Report'},
            {type: 'Amendment of Supplementary Holiday Illness Medical Report'},
            {type: 'Amendment of Supplementary Other Medical Report (to type)Request for Amendment of Supplementary MEDCO GP Medical Report with Review of Records'},
            {type: 'Amendment of Supplementary Re-examination(Report Rejected) MEDCO GP Medical Report with Review of Records'},
            {type: 'Amendment of Supplementary Re-examination(Prognosis Exceeded) MEDCO GP Medical Report with Review of Records'},
            {type: 'Amendment of Supplementary Non-medco GP Medical Report with Review of Records'},
            {type: 'Amendment of Supplementary Re-examination(Report Rejected) Non-medco GP Medical Report with Review of Records'},
            {type: 'Amendment of Supplementary Re-examination(Prognosis Exceeded) Non-medco GP Medical Report with Review of Records'},
            {type: 'Amendment of Supplementary Specialist Orthopaedic Medical Report with Review of Records'},
            {type: 'Amendment of Supplementary Re-examination(Report Rejected) Specialist Orthopaedic Medical Report with Review of Records'},
            {type: 'Amendment of Supplementary Re-examination(Prognosis Exceeded) Specialist Orthopaedic Medical Report with Review of Records'},
            {type: 'Amendment of Supplementary Specialist Psychological Medical Report with Review of Records'},
            {type: 'Amendment of Supplementary Re-examination(Report Rejected) Specialist Psychological Medical Report with Review of Records'},
            {type: 'Amendment of Supplementary Re-examination (Prognosis Exceeded) Specialist Psychological Medical Report with Review of Records'},
            {type: 'Amendment of Supplementary Specialist ENT Report with Review of Records'},
            {type: 'Amendment of Supplementary Specialist Surgeon Report with Review of Records'},
            {type: 'Amendment of Supplementary Specialist Dental Report with Review of Records'},
            {type: 'Amendment of Supplementary Specialist Gynaecology Report with Review of Records'},
            {type: 'Amendment of Supplementary Specialist Neurology Report with Review of Records'},
            {type: 'Amendment of Supplementary Holiday Illness Medical Report with Review of Records'},
            {type: 'Amendment of Supplementary Other Medical Report (to type)'},
            {type: 'Addendum of Specialist Plastic Surgeon Report with Review of Records'},
            {type: 'Addendum of Specialist Plastic Surgeon Report'},
            {type: 'Amended of with Review of Records Specialist Plastic Surgeon Report with Review of Records'},
            {type: 'Amended of with Review of Records Specialist Plastic Surgeon Report'},
        ],
    }
  },
  methods: {
      ...mapActions([
      'refreshCurrentCase',
    ]),
      quality_assurance_swal(failed_numbers){
          Swal.fire({
            title: 'Quality Assurance Checks',
            html: this.parse_failed_checks(failed_numbers),
          })
      },
    requestPDF(return_content){
        const current_case_object = JSON.parse(sessionStorage.getItem('current_case_object'))
        var doc = new jsPDF('p', 'pt')
        let logoData = "data:image/jpg;base64,/9j/4AAQSkZJRgABAQEAZABkAAD/4gKwSUNDX1BST0ZJTEUAAQEAAAKgbGNtcwQwAABtbnRyUkdCIFhZWiAH5AADAAEAFgABAA9hY3NwQVBQTAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA9tYAAQAAAADTLWxjbXMAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA1kZXNjAAABIAAAAEBjcHJ0AAABYAAAADZ3dHB0AAABmAAAABRjaGFkAAABrAAAACxyWFlaAAAB2AAAABRiWFlaAAAB7AAAABRnWFlaAAACAAAAABRyVFJDAAACFAAAACBnVFJDAAACFAAAACBiVFJDAAACFAAAACBjaHJtAAACNAAAACRkbW5kAAACWAAAACRkbWRkAAACfAAAACRtbHVjAAAAAAAAAAEAAAAMZW5VUwAAACQAAAAcAEcASQBNAFAAIABiAHUAaQBsAHQALQBpAG4AIABzAFIARwBCbWx1YwAAAAAAAAABAAAADGVuVVMAAAAaAAAAHABQAHUAYgBsAGkAYwAgAEQAbwBtAGEAaQBuAABYWVogAAAAAAAA9tYAAQAAAADTLXNmMzIAAAAAAAEMQgAABd7///MlAAAHkwAA/ZD///uh///9ogAAA9wAAMBuWFlaIAAAAAAAAG+gAAA49QAAA5BYWVogAAAAAAAAJJ8AAA+EAAC2xFhZWiAAAAAAAABilwAAt4cAABjZcGFyYQAAAAAAAwAAAAJmZgAA8qcAAA1ZAAAT0AAACltjaHJtAAAAAAADAAAAAKPXAABUfAAATM0AAJmaAAAmZwAAD1xtbHVjAAAAAAAAAAEAAAAMZW5VUwAAAAgAAAAcAEcASQBNAFBtbHVjAAAAAAAAAAEAAAAMZW5VUwAAAAgAAAAcAHMAUgBHAEL/2wBDAAMCAgMCAgMDAwMEAwMEBQgFBQQEBQoHBwYIDAoMDAsKCwsNDhIQDQ4RDgsLEBYQERMUFRUVDA8XGBYUGBIUFRT/2wBDAQMEBAUEBQkFBQkUDQsNFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBT/wgARCABkAUADAREAAhEBAxEB/8QAGgABAAMBAQEAAAAAAAAAAAAAAAYHCAUEA//EABsBAQEAAwEBAQAAAAAAAAAAAAABBAUGAwIH/9oADAMBAAIQAxAAAAHVIAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAIDrMHpe3pLM3KAAAAAAAAAAAAAAAAAAGZNDz0k9si89xuI374vCy8CZYey5njkRZLPUAAAAAAAAAAAAAAAUzu+OhWViwjH2Mi9PLv8Atj2dqt7RGu3PALSi+lzukdq0YuVc+JDa9RP48Z6Cta1DLnSzmFkxd6gAAAAAAZD7/wDIPrr9zLdJ1Ur+fqlt5zd16ff1tqt95jQstYJV9XjGZq1ZGVa3HLh2zYMufbOKXpFpLT6c4oCzec+gAAAAAAMed5+UWXp+kvjm+zjvvi5S6nh710vRQjU7/wAhpxc2pAansC8VyTZ0z2GsZcsWTGL+WjkqOrSihrN6T6AAAAAAAx13X5XZeo6K+uc7KO5GHlLquFvXR9PHNTvqgq0Isoy5VmEeNcy4Ysnp6y8JaAsmcX4uekrOpGV8m759AAAAAAARDO1fU8cnt4+X87IXm62TYub7PP2gqdJZccAjKdlYclS1ecU9XVi6l9Z2z4EFSQr4yWAAAAAAAAAAAAAAhZm6z1g0bLLQAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAf/EAC0QAAEEAgEABwgDAAAAAAAAAAUCAwQGAQcAERIUFhcwNRAVITI0NkBQJWBw/9oACAEBAAEFAv60TtGIr4Y8kor9MVS5CI05pySWW4ltLtmGt8zcEqyPnoIx7EbTXxlaumbDP/QHLRDlKlWic1FVIdkZi/K3yuyExRtotTtkcEGJISTXrsUJHZkxkfFKbImvuovRpKqzf/eMjOejBvZDuXu+xzniCZ5S7OSNlLXcCQg2jYuGgMu+HVpLTlixcvYhZ9SbybTms7AVNlef08bHySioOviDuZVRYFClvuOcoSMSRd9FxRRGijYxQvFq4uFI2eQXjlZjwHystdRlxlp6i5s5yTRGsIU72NjsryUIeqbinq5f/ueuAHLFPj63FspUnC0tg6qDUZcqj43GejPn9PKFn+V5YvQua7+h2d6trX17mzUZwXBA3T8vwxIc8MSHBYrsoI2OQKJ4sBnsYOmzzLkeOiJHv/3PqzGOvzYp5+LmvAXbBPn65iwR/wCDQvVeWL0Lmu/odnQHOuKKyQ0sLdihQ1dK8o6NjyJAyYjZZNKCN2LEm8/HEuG8OlJ2EYThnZBZC63ZY9jj3/7n1Z83NmjnMSgZ2QAllLcTsuHWlMO+e/Uxkl4cFhivYtCXUZpYjOYA6OMYeZRIadoYR1Q+pihjvCIGAWz4fhOQaqKHObFMvD4NPAMWAh3ACcu4AeDe1jhXvWbWhpGQNCwhHseYbktOUII4saAgCMyaqKmP/mWuvd4Rz9ZMj31psziIdNMkl1yus12H/gn/xAArEQAABAQFAwMFAAAAAAAAAAAAAQIDBAUREhAhM1BxMkHBEzFRNGBwobH/2gAIAQMBAT8B+2nIm06JDT3qZbO7VKzIxCkal1+B7A4pks7gcyLskMPJfRcnY4ydtVNCEXU7mISYxESv06kki+AszP3BgxLOhXOx2iVtqU8dpdgUE4o8zoHIJLbal17BRiUdC+fGx0Ej1VcYRWgvgKEn6F8+NkkmqrjCM+nXweEo018+NjclsK4q5Sf6GIRmG0ipgZVKhg5bDHnb+zDTSGU2oLL8c//EACkRAAEDAQYGAgMAAAAAAAAAAAEAAgMEBRAREjJQExQhMTNxQVEiYHD/2gAIAQIBAT8B/WpqzI7KwKnqeN0I67PJHg44qmjPEzfVwgkPwhRH5cpYjE7KdjjsjiAGYqShp6aP8WpoA7XBV2obHiq14bGMVzLG9kypc94bgmhWhqbslp+Me7oPK1BWjqbslpeMe7qfzN93Wjrbsba2dgyhylnkm1m4HDqFzs/2nyOkOZ385//EAEEQAAIBAwEEBQcICAcAAAAAAAECAwAEERITITFBEBQiUbEFMmFxc8HRNEBScoGRk6EVM1BiosLh8CNDYHCDkvH/2gAIAQEABj8C/wBNNDAgcocFm4UY2XZygZ9B/Y9xFJkEOTv5jvpZRnZwglj9mMVlmCjvJrdcrL7PtV2LZsfvNg1tU3ciDyNNdMm1bUFWPONRNNbdU2GEL6tpn3fsExCxiuwh7Mk28fZWyt2S0j4BbdAuKzLK8p75GLdN5M+dEfbOPVSDZ7C2j3onP1mjPalRIV09oZ3VZWszRbKViGxHv80mpLid9nFGMljRFki20PIuNTn3Vnrmr0GNfhSWl+ixTPuSVPNY93orJ3CjH5MVBEP89xnV6q19bOn2a48K/XR/himiuWVoBGTlUxvyKltrdohEoUjUmeVQySIsvlNiymNdyjf5x+zFO8d0EbG5EjXGamuVhNy0S50A4z30dmYrZeQRMn86z13PoMa/Co7Tygiq0h0pNHuGe4j5jsraIyvxwKzO8Vsnr1N/f21dT7aSWWOMleQzXac1exSduNn0kHuxVvHaQiFGiyQO/Jp4rqITRiItg9+RSTw2ixypvVsndVnZL5hzK/gPfSfpKZIbVBqIc4Dnu/vuow7TyfHuwrR6VK+qmXUGwcal4Gnuhvkks8k+sb6QStoiLDW3cOZrq2yXYadGzxuxUixNriDEI3eORqwZ/O2ePhVx9VPCtgjCONBqkfuFLqe4kcHOtnHwoqwyp3EGilxNDJJnhcS6iPRirhLcWsVxoOzaCLSdXLgKyPmM3sveOi+9k3Rd+1HhVr7H3mpPYHxHRatyaHd9hPxpreGWOJwuv/E518qtv4vhXyq2/i+FQ+T7jTLpi2T44Gp7aO4W5jQ4Dr4H011QXM+x06dON+PXxpdUT2ttntSyLp/6g8ajhjGmONQqj0VcfVTwryqeeIv5+iLyfbuYta65GU4JHIeNdXjcRKBqdzyFXFwb2YtFGz8ABuHzKb2XvHRfexbou/a+6rS9AzEAYnPceXvoXNqwWTGO0MgirKCV40ieTDLGmM0DCAbqA6k/eHMUskZe3uIjzGCp9VYaG2dvpaT8aKNcCBDxFuNP58eiS2uDqniOGbjqPfXnQN6TFQLrbSL3aCPfTNGNlPH+shJzp7j6quPqp4V5U/4v5+i2vguYimyY/ROd3jRntwjZXSyvwIpbFY1RZSBsoRvenjcaXQ6WB5H5g0j2/aY5OlyKbq0OgtxOcnoZHAZWGCDzrPVz+I3xrY20ezTjTRyoJI2GGVhkGtXVCv1ZWHvpZYLQCReDMSxH39Gq6tUlfhr4N99fJn/Gf40rw2abReDP2iPvq3toGMbXJbU6/RGN35ipI7iVkjjXXpTi++vkzfjP8atxZuweTOqAtqwO+rr6Ox3/AH0Z7m1WWU8WJNSdUgEO0xqxzx/70NFKiyRsMMrDINauqkehZWA8aJtLZY3O7Xxb76eaWzR5HOWOTv8AnuzVglxGdUbNw9VbrO5DjhJb5P5rWgjytj0bQVk2zRZ4yXJ0/wBaMaHaTPvklx539P8AYX//xAAqEAEAAQMDAwMEAgMAAAAAAAABEQAhMUFRYXGBkRCh8EBQscHR8SBgcP/aAAgBAQABPyH/AFqUzB8tQCsN1oyOsfZyBCDqmTuqHNpRVQ909qTG92EFSPs09y1X7uP4CfzQQW/VqFmxOvDfgl7Uxh0YUIiG/wBhV6gCSbjMdytBzlejUovusTy0pHpkSSDnBNiro5UstdXE8GJc0ryDt5I/qnByuKBZM7hRAviJrR49heQ6Ol+tSZ21oSVGL0iHJ8dKBkAurpT+ji68zgOszxVvX4rQTJy1Qik5EQLnVo1xROuFvNYVmiFRsDg3naalMG4kWLi+9SbPzMap4Je1qT9spdWU+CpiXSNBhVCkWOVuePoQg7vQIN79aB7MS8RajDmnAYMxn3rLE2mDxQX3EtRkqXgGVmFN+lC8DMm4t1p/9oZFCb7LUioG6ynx9qZFFpOCfeaM08+pmisoCk4NTin0RBZmF/moJMJYv5OCaAi8OOIjpV63czGtzWSKO+IeoLLuBXzW2nklHJ2oNVf3tUFPog5mIIR2o/BUCybUO9pjmm3RxcXdan8ysONQTfekJES4mn0E6k6n0PhtvT4Tb/gsXZOl8l+HmnSHuMAQtBzX9hR/YUWKGVwxDUkaYXN7MQZGLdMEVIYB2tlnemqyyyjgT1Y5ringoIK+a20aLcK/HPoSmz8CBdrS7c1OlMudKxqym1Q39sqo3ssd/ovffQ+E29B43403qsQp859m9CxCZIGieKCrKwzaVXxTKiC2k1eYHqFWEh+givcaMhmoZ7V3ojJO591FQGFM0eHSM/InPegROOV7JWqzc49ylk4CYSmB1UN+Gvktte09BhUI9BMusvFM0YrWQOjxUnKoppsKuPGL0kd3JAwn0EU10Br0GmWVuqY2l9HIkGkDkp3DnQqEwTyBVXdXNJslFhslK0h0L8FEMXL4bkmPQKKEIWNoXpdmoDFpM5m4yhqZrIIcqWkvaGjSKTBtJ0N9b6Z9LBI0VqWJtybl3S2GkOTHyRj90XwwATBBhrkfmuSMvL0tGnWGyUiT3+BChZclchtKWKtnjUlvZ+tA42+yiFcP8N4ocYAvdMXs1ttNjeS9Rmr/ACBH9anzUXBRg4EsHLv/AMF//9oADAMBAAIAAwAAABCSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSQ2SSSSSSSSSSSSSSSSSSQz7QOSSSSSSSSSSSSSSSTDq+RzBjwPuABySSSSSSRuaESOcUDABzvySSSSSSQCb/6KfgSAacPySSSSSSReX7hsSCSQKcTySSSSSSSiQUOSOMOISRiSSSSSSSSSSSSSSISCSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSST/xAAqEQACAgADBgUFAAAAAAAAAAABEQAQITHwQEFRYYGhIFBxkbEwYHDB8f/aAAgBAwEBPxD7adiagzJBHycOK0GRy/hfuEgGYPQD6Y/EGxL1IB7Md50VEcDT8hLF3FEw9QgWOomDwiUKe5MsjN4I84NRk+pJ+YWFdVyjoGnHHTjjghjjpxx7A0HrOjiJgqD3PtgO/SOxJBIYJ8cn3XKHO+ES7RIYKMH0DSvDYWgEa2YruHxCc0nJDBRpRXjFRgo0thzmm5itz0ChxNMENOGnHbjowUaewlWNOaIdgQIJOazLJPuWaAYDBhIkWjnApbTfmaXgVGCKGDwryBTGL8Df/8QAKhEAAgECAgoBBQAAAAAAAAAAAREAECGBoSAxQEFQUXGxwfCRYGFw0fH/2gAIAQIBAT8Q+miEYW86oAioHweDlG5jCgCwbFhLN4QAmwh9W9bQzUYD+cEMgWm9JkYnUcIBFxaD3YBDKaoLpaAXoyPmKioooqKKKGKKKiii2ESDV/BhEtJPwPcIhQAkdfcIAQV0vMENBDL6YhjpeX2FiF7uRpnBBmS8wQ0FHHW0dBDQUexe99jTKu9Mh5MFFBRRVUVBDQUWwiNgOYB7iJ7y6DtQhAiIgAF2j9R3WaPQdBDHBDovgDlo/wADf//EACUQAQEAAgIBBAMAAwEAAAAAAAERACExQVEQYXGBQJGhUGDwcP/aAAgBAQABPxD/AFpbbHGnkAsdVTY6TaE2anFirYilHpIu5/hg60ulAT2BGndORwGSFDZG8VuMkPNDEOVXRgVIcS/ENX7ykY8P3ACfSycGcuIFKckRHseuMKCAEwRKGAvpY4LDDQsWr/rBt6/wJW7qAMTDTeyxPOBapLG7aBR8iNbly/rcfNV9CnRgYKgBesFBYecG+iq2kDoNGjkVcQG9b0Gqbp3lsn4oJ0XlR1Tujj49YcAHKlADaoG3KLmPANRdPQjywrKHm38wv9wYbwFli5aAGqdbIJ+RUoA5V6MRfwyfq0TyNAjMFVXM5tkvu98AGt5N/Rk7r1oES5mn29smfHBvGDtcdi4SIku6AO1AQWDF5V9yBMs5T74JdhsSFRARYLEBYKsusoHjbPc+DAYcbt36LiQ+EIowsVoaVBBv8D64+LyOvSlAFBz3kkcvIdamE96fbB4pSUEgKb0x7YJPC7/S1jqqlIjclBrx5w2Gjp2AegfWF7qMAE2Dwv3jv7lVNSo4H3mglqQoBnZtfJ9Br37Gi11agikcLk3aKaTQYkYyxmxyUx7ZQl/KUfCYqmTNAUeQX9YddxTeSjjYvUwwHqz/AElOGdVBB9ewCvdysncyL1vupe76GypnprqHpaAoQddEGr0gTgfxRTOVd5dPkxRFHYjMutRcaYnYECyAoqlQC8pEsogESItxALiUUcI9P4HyYhH0/wD63nh6EP4fr/Nfu3dqp+P4sJzESoAqbq/A+rlyafuhZCUGIvQ4mhKxI1oAai6DsuRF4BVaIHrNa4a4wzn10fO0OAjftEwgx7NlB+g9DZAJJu0Fh9V+30fwdUqyGxLQ704QhmXdlTRlgBRtbqIfsBMhAgSble+PP4HPqPCxLt/v0SkYnc3dmDu294Ia9g5GCq/jOXWpRaR0RMOvXnTVQrjsYusjyAF2hALqJQVLDyUzIm0ooLYokcNbEfk5EX4mKOcEXbh1HkCJpIplTEB4PnKok9AgfMFm16O6ZK4Anv5m/QYEBNc54NX5j94rlJHwoA0cg2SCeiv/AIvn0dGR1CP2Ex8s7K+0yE3QERCI/ThPOqe2XLQKAOShnNDjoSvcRPr8BolBlWrCFVdGDkIHwaUqF3DXpPKxJUQeRFMVT0scPg4YFetosBQVQCrwGHd8IuRRpHw4xqLMfgAZo7U9qUobdm/S8ndYXSsmqyzb5xDCrYEfrIB5TrcK/II5bprAGDG1ujod5pABZYJQ+4DQRTAJMykBoOshSxgg9GzQGJPFbf0T94ymWsACAaAOMYTG95a6cdPn0Z6IIvpRpMcflj3xCZfBn9pa6EFBjDxiXypUvKAKzcNte/zXSgcVZM2GgpYkNDTHyjnVVX43hWNOkJ9H9ZtE2i73UXzdyc8G76RvsgylVL/4J//Z"
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

        doc.text(40, 120, doc.splitTextToSize(this.appointmentData.slot.expert, 520), {align: "left"})
        doc.text(40, 130, this.appointmentData.slot.expert_address.split(', '), {align: "left"})

        doc.setFont('times','bold')
        doc.text(40, 205, doc.splitTextToSize('Date: ' + moment().format('DD/MM/YYYY'), 520), {align: "left"})

        doc.text(40, 230, doc.splitTextToSize('Our Ref: ' + our_ref, 520), {align: "left"})
        doc.text(40, 245, doc.splitTextToSize('Solicitor Ref: ' + current_case_object.instructing_party.instruction_party_reference, 520), {align: "left"})
        doc.text(40, 260, doc.splitTextToSize('Solicitor: ' + current_case_object.instructing_party.name, 520), {align: "left"})
        doc.text(40, 275, doc.splitTextToSize('MedCo ID: ' + current_case_object.instructing_party.medco_id, 520), {align: "left"})
        doc.text(40, 290, doc.splitTextToSize('Claimant: ' + current_case_object.claimant.title + ' ' + current_case_object.claimant.first_name + ' ' + current_case_object.claimant.last_name, 520), {align: "left"})
        doc.text(40, 305, doc.splitTextToSize('Accident Date: ' + moment(current_case_object.accident.date).format('DD/MM/YYYY'), 520), {align: "left"})

        doc.setFont('times', 'normal')
        doc.text(40, 350, doc.splitTextToSize('Dear ' + this.appointmentData.slot.expert + ','), {align: "left"})

        doc.setFont('times','normal')
        doc.setFontSize(12)

        var paragraph_1 = 'Many thanks for providing us with a medical report for the above named claimant. However, the solicitors have issued a request for ' + this.selected_request_type + '.'
        doc.text(40, 390, doc.splitTextToSize(paragraph_1, 520), {align: "left"})

        var paragraph_2 = 'We enclose a letter from the solicitor, which we believe to be self-explanatory'
        doc.text(40, 430, doc.splitTextToSize(paragraph_2, 520), {align: "left"})

        doc.setFont('times','bold')
        var paragraph_3 = 'Please email your ' + this.selected_request_type + ' to reports@integramedical.co.uk'
        doc.text(40, 470, doc.splitTextToSize(paragraph_3, 520), {align: "left"})

        doc.setFont('times','normal')
        var paragraph_4 = 'If you consider the request unwarranted please advise by way of a brief letter.'
        doc.text(40, 510, doc.splitTextToSize(paragraph_4, 520), {align: "left"})


        var sla_days = 'N/A'
        if (this.selected_request_type.includes('Amendment with Review of Records')){
            sla_days = this.appointmentData.slot.expert_sla_addendum
        }else if(this.selected_request_type.includes('Amendment')){
            sla_days = this.appointmentData.slot.expert_sla_amendment
        }else if(this.selected_request_type.includes('Addendum')){
            sla_days = this.appointmentData.slot.expert_sla_addendum
        }else if(this.selected_request_type.includes('Part 35')){
            sla_days = this.appointmentData.slot.expert_sla_part_35
        }else if(this.selected_request_type.includes('Comments')){
            sla_days = this.appointmentData.slot.expert_sla_comments
        }

        var paragraph_5 = 'We thank you for your assistance and look forward to receiving the report withing the next ' + sla_days + ' days.'
        doc.text(40, 550, doc.splitTextToSize(paragraph_5, 520), {align: "left"})

        doc.text(40, 600, doc.splitTextToSize('Yours faithfully,', 520), {align: "left"})
        doc.text(40, 620, doc.splitTextToSize('Integra Medical Reporting', 520), {align: "left"})


        if(return_content){
            var document_name = "Request for " + this.selected_request_type + "IP Ref= " + current_case_object.instructing_party.instruction_party_reference+'.pdf'
            var document_list = []
            document_list.push(doc.output('blob'))
            document_list.push(document_name)
            console.log('content to be returned')
            return document_list
        } else {
            doc.save("Request for " + this.selected_request_type + " - Our Ref= " + our_ref + "- Solicitor's Ref= " + current_case_object.instructing_party.instruction_party_reference+'.pdf')
            window.open(doc.output('bloburl'), '_blank')
        }
    },
    deleteRequest(id){
        Swal.fire({
            title: 'Are you sure?',
            text: "You won't be able to revert this!",
            type: 'warning',
            showCancelButton: true,
            confirmButtonColor: '#3085d6',
            cancelButtonColor: '#d33',
            confirmButtonText: 'Yes, delete it!'
            }).then((result) => {
                if (result.value) {
                    this.$http
                        .delete(this.url__request_verbose+id)
                        .then(response =>{
                            Swal.fire(
                            'Deleted!',
                            'Your request has been deleted.',
                            'success'
                            )
                            this.refreshCurrentCase();
                        })
                        .catch(function(error) {
                            console.log(error);
                            Swal.fire(
                            'Request could not be deleted!',
                            error,
                            'error'
                            )
                        });
                }
            })
    },
      getRequestTypes(searchTerm) {
        var product = this.currentAppointment.product_name.toLowerCase()
        if (product.includes('medco') && !product.includes('non')){
            this.request_types_filtered = new Promise(resolve => {
                window.setTimeout(() => {
                    if (!searchTerm) {
                        this.request_types_filtered = this.request_types.filter( x  => {
                            return x.type.toLowerCase().includes(product) && !x.type.toLowerCase().includes('non');
                        }).map(x => x);
                        resolve(this.request_types_filtered);
                    } else {
                        const term = searchTerm.toLowerCase();
                        this.request_types_filtered = this.request_types.filter( x  => {
                            return x.type.toLowerCase().includes(term) && x.type.toLowerCase().includes(product) && !x.type.toLowerCase().includes('non');
                        }).map(x => x);
                        resolve(this.request_types_filtered);
                    }
                }, 500)
                });
        }else{
            this.request_types_filtered = new Promise(resolve => {
                window.setTimeout(() => {
                    if (!searchTerm) {
                        this.request_types_filtered = this.request_types.filter( x  => {
                            return x.type.toLowerCase().includes(product);
                        }).map(x => x);
                        resolve(this.request_types_filtered);
                    } else {
                        const term = searchTerm.toLowerCase();
                        this.request_types_filtered = this.request_types.filter( x  => {
                            return x.type.toLowerCase().includes(term) && x.type.toLowerCase().includes(product);
                        }).map(x => x);
                        resolve(this.request_types_filtered);
                    }
                }, 500)
            });
        }
        },
      handleFileUpload() {
        this.file = this.$refs.file.files[0];
        const Done = Swal.mixin({
          toast: true,
          position: 'center',
          showConfirmButton: false,
          timer: 1500
        });
        Done.fire({
          title: 'Finished coding, file attached!'
        })
      },
      base64ToArrayBuffer: function(base64) {
        var binary_string =  window.atob(base64);
        var len = binary_string.length;
        var bytes = new Uint8Array( len );
        for (var i = 0; i < len; i++)        {
            bytes[i] = binary_string.charCodeAt(i);
        }
        return bytes.buffer;
    },
      parse_failed_checks(failed_numbers){
          var quality_assurance_checks =
            {
            '1': "The expert has listed their qualifications",
            '2': "The expert has listed the purpose of the report",
            '3': "The report contains Claimant's correct Title",
            '4': "The report contains Claimant's correct First name",
            '5': "The report contains Claimant's correct Last name",
            '6': "The report contains Claimant's correct Date of Birth (DOB)",
            '7': "The report contains Claimant's correct Date of Accident (DOA)",
            '8': "The report lists details of all key documents or other evidence which the expert has been provided with",
            '9': "The report follows a chronological order",
            '10': "The report has the matters of fact and opinion clearly distinguished and these are kept separate",
            '11': "The expert clearly states the source of Statements of Fact that are relied upon",
            '12': "The report is non-provisional",
            '13': "The overall style, size and tone of report is more focused on analysis and opinion than history and narrative",
            '14': "Part 35 of the Civil Procedure Rules and the Practice Direction is included",
            '15': "The report includes a declaration to the court",
            '16': "The expert has provided an opinion within the scope of their competence",
            '17': "The expert has not identified unfamiliarity with the instruction",
            '18': "The expert has checked and stated the claimant's photo identification and type",
            '19': "The report contains Claimant's correct Address",
            '20': "The report contains Claimant's correct MedCo Reference",
            '21': "The report contains Claimant's correct Instructing Party Reference",
            '22': "The report contains Claimant's correct Precise examination location",
            '23': "The claimant's Gender throughout the report is correct",
            '24': "The expert has provided a description of the claimant's occupation",
            '25': "There was no third party present or there was a third party noted in attendance and the expert states the name of the individual attending and employer (if applicable)",
            '26': "The expert has set out any assumptions made",
            '27': "The expert has set out any calculations made",
            '28': "The language of the report does not advocate for the instructing party",
          }

          var failed_checks_html = '<h3><u>Failed checks:</u></h3><ul style="text-align: left">'
          if (failed_numbers) {
              var split_numbers = failed_numbers.split(',')
              for (var i in quality_assurance_checks) {
                  if (split_numbers.includes(i)) {
                      failed_checks_html += '<li><span style="color: red; font-size: 15px">' + quality_assurance_checks[i] + '</span></li>'
                  }
              }
                failed_checks_html += '</ul>'
          }else{
              failed_checks_html += '<li><span style="color: red;">N/A</span></li><br>'
              failed_checks_html += '</ul>'
          }
          return failed_checks_html;
      },
      downloadAttachment(id) {
        this.$http
            .create({headers: {'Content-Type': 'application/json'}})
            .get(this.url__attachment+id)
            .then(response =>{
                var arrBuffer = this.base64ToArrayBuffer(response.data.content);
                var blob = new Blob([arrBuffer], {type: response.data.mime})
                var url = window.URL.createObjectURL(blob)
                var a = document.createElement("a")
                document.body.appendChild(a)
                a.style = "display: none"
                a.href = url
                a.download = response.data.filename || 'Report.unknown'
                a.click()
                window.URL.revokeObjectURL(url)
            })
            .catch(function (r) {
                Swal.fire("Error downloading attachment.<br> Actual Error: " + r)
            });
    },
    completeRequest(id, completed){
        this.$http
            .patch(this.url__request_complete, {'id': id, 'completed': completed})
            .then(response =>{
                this.refreshCurrentCase();
                Swal.fire(
                    'Good job!',
                    'Request updated!',
                    'success'
                )
            })
    },
    viewAttachment(id) {
        this.$http
            .get(this.url__view_attachment+id)
            .then(response =>{
                window.open(response.data.presigned_url)
            })
            .catch(function (r) {
                Swal.fire("Error downloading attachment.<br> Actual Error: " + r)
            });
        },
        applyChecks: function(request, amroc_status, amroc_failed_checks, clinical_quality_checks){
            if (this.selected_request_type === ''){
                NProgress.done()
                Swal.fire(
                    'ERROR',
                    'Please select a Request Type',
                    'error',
                    )
            }else if (!this.date_request_received){
                NProgress.done()
                Swal.fire(
                    'ERROR',
                    'Please select a Request Received Date',
                    'error',
                    )
            }else if (this.file === ''){
                Swal.fire({
                    title: "Are you sure?",
                    text: "Are you sure you don't want to attach the IP email/letter?",
                    type: "warning",
                    showCancelButton: true,
                    confirmButtonClass: "md-button md-success btn-fill",
                    cancelButtonClass: "md-button md-danger btn-fill",
                    confirmButtonText: "Yes, proceed!",
                    buttonsStyling: false
                }).then(result => {
                    if (result.value) {
                        this.email_template(request, true, amroc_status, amroc_failed_checks, clinical_quality_checks)
                    }else{
                        NProgress.done()
                        console.log(this.selected_request_type)
                        Swal.fire(
                            'ERROR',
                            'Please Upload the Instructing Party Request Email/Letter',
                            'error',
                        )
                        return
                    }
                });
            }else{
                this.email_template(request, true, amroc_status, amroc_failed_checks, clinical_quality_checks)
            }
        },
      email_template: function(request, checks_passed=false, amroc_status=false, amroc_failed_checks='', clinical_quality_checks=''){
          console.log('amroc_status ', amroc_status)
          console.log('amroc_failed_checks ', amroc_failed_checks)
          NProgress.start()
          if (request){
              var extra_html_content = "";
              (async () => {
                const { value: text } = await Swal.fire({
                  input: 'textarea',
                  inputPlaceholder: "Type your free text that you want to add to the request's email...",
                  inputAttributes: {
                    'aria-label': 'Type your free text here'
                  },
                  showCancelButton: true
                })

                if (text) {
                  extra_html_content = text;
                }
                var form_data = new FormData()
                  form_data.append('regards_to_prog', this.regards_to_prog)
                    Swal.fire({
                        title: 'Emails',
                        input: 'text',
                        inputValue: this.appointmentData.slot.expert_email + ',' + this.appointmentData.slot.secretarial_email,
                        inputPlaceholder: 'Enter your email address'
                    }).then(result => {
                        if (result.value) {
                        form_data.append('request_id', request.id)
                        form_data.append('additional_emails', result.value)
                        if (extra_html_content){
                            form_data.append('extra_html_content', extra_html_content)
                        }
                        this.$http
                            .post(this.url__email_expert_for_request, form_data)
                            .then(response => {
                                NProgress.done()
                                console.log(response.data)
                                Swal.fire(
                                    'Good job!',
                                    'Expert has been notified!',
                                    'success'
                                )
                                this.refreshCurrentCase();
                            })
                            .catch(function(error) {
                                NProgress.done()
                                console.error(error.response);
                            });
                        }else{
                            NProgress.done()
                        }
                    })

                })()

          }else{
            if (checks_passed){
                var form_data = new FormData();
                form_data.append('regards_to_prog', this.regards_to_prog);
                form_data.append('quality_assurance_status', amroc_status)
                if (clinical_quality_checks){
                    form_data.append('clinical_quality_checks', clinical_quality_checks.toString())
                }else{
                    form_data.append('clinical_quality_checks', clinical_quality_checks)
                }
                if (amroc_failed_checks){
                    form_data.append('quality_assurance_failed_checks', amroc_failed_checks.toString())
                }else{
                    form_data.append('quality_assurance_failed_checks', amroc_failed_checks)
                }
                const request_pdf_document = this.requestPDF(true)
                form_data.append('request_pdf_document', request_pdf_document[0])
                form_data.append('request_pdf_document_name', request_pdf_document[1])
                var selected_file_ids = []
                for (var index in this.selected_documents){
                    selected_file_ids.push(this.selected_documents[index].id)
                }
                form_data.append('selected_file_ids', selected_file_ids)
                form_data.append('appointment', this.appointmentData.id)

                form_data.append('request_type', 'Request for ' + this.selected_request_type)

                form_data.append('notes', this.notes)
                form_data.append('case', this.id)
                form_data.append('additional_emails', this.additional_emails)
                form_data.append('date_request_received', this.date_request_received)

                try {
                    form_data.append('file', this.file)
                }catch (err){
                    NProgress.done()
                    console.log('Error:',err)
                }
                var html_list = '<div>'

                for (var index in this.selected_documents){
                    html_list += '<li>' + this.selected_documents[index].type + '</li>'
                }
                html_list += '</div>'

                for (var entry of form_data.entries()){
                    console.log(entry[0] + ', ' + entry[1])
                }

                Swal.fire({
                    width: '1000px',
                    title: 'Our ref: ' + this.currentCase.claimant.last_name.substring(0, 3) + this.currentCase.id + ' - ' + this.selected_request_type,
                    html: '<div class="md-layout-item md-size-100" style="text-align: left">'
                        + '<body>'
                        + '<div>'
                        + '</div>'
                        + '<div>'
                        +  '</br><b>Our Ref:</b> ' + this.currentCase.claimant.last_name.substring(0, 3) + this.currentCase.id
                        +  '</br><b>Solicitor Ref:</b> ' + this.currentCase.instructing_party.instruction_party_reference
                        +  '</br><b>MedCo Case ID:</b> ' + this.currentCase.medco_id
                        +  '</br><b>Claimant:</b> ' + this.currentCase.claimant.title + ' ' + this.currentCase.claimant.first_name + ' ' + this.currentCase.claimant.last_name
                        +  '</br><b>Accident Date:</b> ' + this.currentCase.accident.date
                        +  '</br>'
                        +  '</br>Dear ' + this.appointmentData.slot.expert + ','
                        +  '</br>'
                        +  '</br>Many thanks for providing us with a medical report for the above named claimant.'
                        +  '</br>'
                        + '<div class="md-layout-item md-size-100 inputBox">'
                        + '<label for="specific_html_content" style="font-size: 12px">Additional Email Content</label>'
                        + '<div class="md-field md-theme-default md-has-textarea">'
                        + '<textarea id="specific_html_content" class="md-textarea">'
                        + '</textarea>'
                        + '</div>'
                        + '</div>'
                        + '</br>'
                        + '</br>However the solicitors have issued a ' + this.selected_request_type + '</b>'
                        + '</br>'
                        + '</br>We enclose a letter from the Solicitors, which we believe to be self-explanatory.'
                        + '</br>Additional attachments:'
                        +  html_list
                        + '</br>Please email your {request_type_name} to reports@integramedical.co.uk'
                        + '</br>We thank you for your assistance and look forward to receiving the {request_type_name} within the next <b>{sla_days}</b> SLA days.'
                        + '</br>'
                        + '</br>Yours faithfully,'
                        + '</br>Integra Medical Reporting'
                        + '</body>',
                    showCancelButton: true,
                    confirmButtonClass: "md-button md-success",
                    confirmButtonText: "SEND EMAIL",
                    cancelButtonClass: "md-button md-danger",
                    buttonsStyling: true,
                    preConfirm: () => {
                    this.specific_html_content = document.getElementById('specific_html_content').value
                    form_data.append('specific_html_content', this.specific_html_content)
                    }
                }).then(result => {
                    if (result.value) {
                        this.$http
                            .post(this.url__email_expert_for_request, form_data)
                            .then(response => {
                                NProgress.done()
                                console.log(response.data)
                                Swal.fire(
                                    'Good job!',
                                    'The expert has been notified!',
                                    'success'
                                )
                                this.refreshCurrentCase();
                                this.selected_documents = []
                                this.selected_request_type = ''
                                this.specific_html_content = null
                                this.file = ''
                                if (this.$refs.file){
                                    console.log(this.$refs.file)
                                    this.$refs.file.value = ""
                                }
                                for (var index in this.outputData.inputItems) {
                                    this.outputData.inputItems[index].selected = false
                                    this.outputData.inputItems[index].visisble = true
                                }
                            })
                            .catch(function(error) {
                                NProgress.done()
                                console.error(error.response);
                            });
                    }else{
                        NProgress.done()
                    }
                })
            }else{
                this.applyChecks(request, amroc_status, amroc_failed_checks, clinical_quality_checks)
            }
          }
      },
    //   autoSave: function(){
    //     for (var index in this.outputData.inputItems) {
    //         if (this.outputData.inputItems[index].selected){
    //             this.selected_documents.push({'id': this.outputData.inputItems[index].id, 'name': this.outputData.inputItems[index].name, 'type': this.outputData.inputItems[index].type})

    //         }
    //     }
    //     console.log(this.selected_documents)
    //   },
      regards_to_prognosis_check(request){
          Swal.fire({
              title: 'Is the request with regards to prognosis?',
              input: 'checkbox',
              width: '600px',
              inputValue: 0,
              inputPlaceholder: 'Yes, mate!',
              confirmButtonText: 'Continue',
              }).then((result) => {
                  console.log(result.dismiss)
                  if (result.dismiss){
                      return;
                  }
                  if (result.value) {
                      this.regards_to_prog =  true;
                      this.send_email(request);
                  } else {
                      this.regards_to_prog =  false;
                      this.send_email(request);
                  }
            })
      },
      send_email: function(request) {
          var amroc_status = null
          var failed_checks = ''
          if (request){
              this.email_template(request)
          }else{
            var claimant_address = []
            if (this.currentCase.claimant.address1){
              claimant_address.push(this.currentCase.claimant.address1)
            }
            if (this.currentCase.claimant.address2){
              claimant_address.push(this.currentCase.claimant.address2)
            }
            if (this.currentCase.claimant.address3){
              claimant_address.push(this.currentCase.claimant.address3)
            }
            if (this.currentCase.claimant.postcode){
              claimant_address.push(this.currentCase.claimant.postcode)
            }
            var listContainer = document.createElement('div');
            var listElement = document.createElement('ul');


            var quality_assurance_html = ''
            listContainer.appendChild(listElement);


            var quality_assurance_form_integer_results = []
            var quality_assurance_dictionary =
            {
                '1': "The expert has listed their qualifications",
                '2': "The expert has listed the purpose of the report",
                '3': "The report contains Claimant's correct Title",
                '4': "The report contains Claimant's correct First name",
                '5': "The report contains Claimant's correct Last name",
                '6': "The report contains Claimant's correct Date of Birth (DOB)",
                '7': "The report contains Claimant's correct Date of Accident (DOA)",
                '8': "The report lists details of all key documents or other evidence which the expert has been provided with",
                '9': "The report follows a chronological order",
                '10': "The report has the matters of fact and opinion clearly distinguished and these are kept separate",
                '11': "The expert clearly states the source of Statements of Fact that are relied upon",
                '12': "The report is non-provisional",
                '13': "The overall style, size and tone of report is more focused on analysis and opinion than history and narrative",
                '14': "Part 35 of the Civil Procedure Rules and the Practice Direction is included",
                '15': "The report includes a declaration to the court",
                '16': "The expert has provided an opinion within the scope of their competence",
                '17': "The expert has not identified unfamiliarity with the instruction",
                '18': "The expert has checked and stated the claimant's photo identification and type",
                '19': "The report contains Claimant's correct Address",
                '20': "The report contains Claimant's correct MedCo Reference",
                '21': "The report contains Claimant's correct Instructing Party Reference",
                '22': "The report contains Claimant's correct Precise examination location",
                '23': "The claimant's Gender throughout the report is correct",
                '24': "The expert has provided a description of the claimant's occupation",
                '25': "There was no third party present or there was a third party noted in attendance and the expert states the name of the individual attending and employer (if applicable)",
                '26': "The expert has set out any assumptions made",
                '27': "The expert has set out any calculations made",
                '28': "The language of the report does not advocate for the instructing party",
            }
            var clinical_quality_assurance_form_integer_results = []
            var clinical_quality_assurance_dictionary =
            {
                '1': "Onset of injury",
                '2': "Onset of injury",
                '3': "Mechanism of injury",
                '4': "No injury at all in report",
                '5': "Past medical/accident history",
                '6': "Inconsistent findings",
                '7': "Physical examination",
                '8': "Prognosis/recovery timeframe",
                '9': "Treatment",
                '10': "Opinion and prognosis are not provided for all injuries relevant to the accident",
                '11': "Report omits facts that do not support the expert's opinion",
                '12': "Clinical opinion not based on claimant's account",
                '13': "Injury falls outside expert's scope of expertise",
                '14': "Referral to specialist",
                '15': "Referral for investigations",
                '16': "Factory produced",
                '17': "Language offensive, derogatory or misrepresented",
                '18': "Sufficient time spent with claimant",
                '19': "Records review required",
                '20': "Expert has requested records"
            }
            Swal.mixin({
                confirmButtonText: 'Next &rarr;',
                showCancelButton: true,
                progressSteps: ['1', '2', '3']
            }).queue([
                {
                title: "Non-Clinical Quality Assurance check<br>Check only the ones that are failing!",
                width: 1200,
                animation: false,
                html:   '<div class="md-layout-item md-size-100" style="text-align: left">'
                        // +'<input type="checkbox" style="display:inline-block;vertical-align:middle;zoom:1.5;" class="md-checkbox" name="assurance_checkboxes" value=3>'
                        // +"<label>The report contains Claimant's correct <b>Title</b> [" + this.currentCase.claimant.title + "]</label>"
                        // +'</input>'
                        // +'</div>'
                        // +'<div class="md-layout-item md-size-100" style="text-align: left">'
                        +'<input type="checkbox" style="display:inline-block;vertical-align:middle;zoom:1.5;" class="md-checkbox" name="assurance_checkboxes" value=4>'
                        +"<label>The report contains Claimant's correct <b>First name</b> [" + this.currentCase.claimant.first_name + "]</label>"
                        +'</input>'
                        +'</div>'
                        +'<div class="md-layout-item md-size-100" style="text-align: left">'
                        +'<input type="checkbox" style="display:inline-block;vertical-align:middle;zoom:1.5;" class="md-checkbox" name="assurance_checkboxes" value=5>'
                        +"<label>The report contains Claimant's correct <b>Last Name</b> [" + this.currentCase.claimant.last_name + "]</label>"
                        +'</input>'
                        +'</div>'
                        +'<div class="md-layout-item md-size-100" style="text-align: left">'
                        +'<input type="checkbox" style="display:inline-block;vertical-align:middle;zoom:1.5;" class="md-checkbox" name="assurance_checkboxes" value=19>'
                        +"<label>The report contains Claimant's correct <b>Address</b> [" + claimant_address.join(', ') + "]</label>"
                        +'</input>'
                        +'</div>'
                        +'<div class="md-layout-item md-size-100" style="text-align: left">'
                        +'<input type="checkbox" style="display:inline-block;vertical-align:middle;zoom:1.5;" class="md-checkbox" name="assurance_checkboxes" value=6>'
                        +"<label>The report contains Claimant's correct <b>Date of Birth(DOB)</b> [" + moment(this.currentCase.claimant.date_of_birth).format('DD/MM/YYYY') + "]</label>"
                        +'</input>'
                        +'</div>'
                        +'<div class="md-layout-item md-size-100" style="text-align: left">'
                        +'<input type="checkbox" style="display:inline-block;vertical-align:middle;zoom:1.5;" class="md-checkbox" name="assurance_checkboxes" value=7>'
                        +"<label>The report contains Claimant's correct <b>Date of Accident(DOA)</b> [" + moment(this.currentCase.accident.date).format('DD/MM/YYYY') + "]</label>"
                        +'</input>'
                        +'</div>'
                        +'<div class="md-layout-item md-size-100" style="text-align: left">'
                        +'<input type="checkbox" style="display:inline-block;vertical-align:middle;zoom:1.5;" class="md-checkbox" name="assurance_checkboxes" value=20>'
                        +"<label>The report contains Claimant's correct <b>MedCo reference</b> [" + this.currentCase.instructing_party.medco_id + "]</label>"
                        +'</input>'
                        +'</div>'
                        +'<div class="md-layout-item md-size-100" style="text-align: left">'
                        +'<input type="checkbox" style="display:inline-block;vertical-align:middle;zoom:1.5;" class="md-checkbox" name="assurance_checkboxes" value=21>'
                        +"<label>The report contains Claimant's correct <b>Instructing Party reference</b> [" + this.currentCase.instructing_party.instruction_party_reference + "]</label>"
                        +'</input>'
                        +'</div>'
                        +'<div class="md-layout-item md-size-100" style="text-align: left">'
                        +'<input type="checkbox" style="display:inline-block;vertical-align:middle;zoom:1.5;" class="md-checkbox" name="assurance_checkboxes" value=22>'
                        +"<label>The report contains Claimant's correct <b>Precise examination location</b></label>"
                        +'</input>'
                        +'</div>'
                        +'<div class="md-layout-item md-size-100" style="text-align: left">'
                        +'<input type="checkbox" style="display:inline-block;vertical-align:middle;zoom:1.5;" class="md-checkbox" name="assurance_checkboxes" value=23>'
                        +"<label>The claimant's <b>Gender</b> throughout the report is correct [" + this.currentCase.claimant.gender + "]</label>"
                        +'</input>'
                        +'</div>'
                        +'<div class="md-layout-item md-size-100" style="text-align: left">'
                        +'<input type="checkbox" style="display:inline-block;vertical-align:middle;zoom:1.5;" class="md-checkbox" name="assurance_checkboxes" value=18>'
                        +"<span title='Note: Photo Id can include: Passport, Driving licence, National identity card, PCO licence card'>The expert has checked and stated the claimant's <b>photo identification</b> and type <span style='color: blue'>(hover over for more info)</span></label>"
                        +'</input>'
                        +'</div>'
                        +'<div class="md-layout-item md-size-100" style="text-align: left">'
                        +'<input type="checkbox" style="display:inline-block;vertical-align:middle;zoom:1.5;" class="md-checkbox" name="assurance_checkboxes" value=24>'
                        +"<span title='Note: This should not be vague e.g. “worker”'>The expert has provided a description of the claimant's <b>occupation</b> <span style='color: blue'>(hover over for more info)</span></label>"
                        +'</input>'
                        +'</div>'
                        +'<div class="md-layout-item md-size-100" style="text-align: left">'
                        +'<input type="checkbox" style="display:inline-block;vertical-align:middle;zoom:1.5;" class="md-checkbox" name="assurance_checkboxes" value=10>'
                        +"<label>The report has the <b>matters of fact</b> and <b>opinion</b> clearly distinguished and these are kept separate</label>"
                        +'</input>'
                        +'</div>'
                        +'<div class="md-layout-item md-size-100" style="text-align: left">'
                        +'<input type="checkbox" style="display:inline-block;vertical-align:middle;zoom:1.5;" class="md-checkbox" name="assurance_checkboxes" value=14>'
                        +"<label><b>Part 35 of the Civil Procedure Rules</b> <a href='https://www.justice.gov.uk/courts/procedure-rules/civil/rules/part35' target='_blank'>(URL)</a> and the <b>Practice Direction</b> <a href='https://www.justice.gov.uk/courts/procedure-rules/civil/rules/part35/pd_part35' target='_blank'>(URL)</a> is included</label>"
                        +'</input>'
                        +'</div>'
                        +'<div class="md-layout-item md-size-100" style="text-align: left">'
                        +'<input type="checkbox" style="display:inline-block;vertical-align:middle;zoom:1.5;" class="md-checkbox" name="assurance_checkboxes" value=11>'
                        +"<label>The expert clearly states the source of <b>Statements of Fact</b> that are relied upon</label>"
                        +'</input>'
                        +'</div>'
                        +'<div class="md-layout-item md-size-100" style="text-align: left">'
                        +'<input type="checkbox" style="display:inline-block;vertical-align:middle;zoom:1.5;" class="md-checkbox" name="assurance_checkboxes" value=12>'
                        +"<label>The report is <b>non-provisional</b></label>"
                        +'</input>'
                        +'</div>'
                        +'<div class="md-layout-item md-size-100" style="text-align: left">'
                        +'<input type="checkbox" style="display:inline-block;vertical-align:middle;zoom:1.5;" class="md-checkbox" name="assurance_checkboxes" value=25>'
                        +"<span title='Note: The third party would be a translator or McKenzie friend. The name of the employer should only be required if the employment firm is featured on the claim.'>There was no <b>third party</b> present or there was a third party noted in attendance and the expert states the name of the individual attending and employer (<b>if applicable</b>) <span style='color: blue'>(hover over for more info)</span></label>"
                        +'</input>'
                        +'</div>'
                        +'<div class="md-layout-item md-size-100" style="text-align: left">'
                        +'<input type="checkbox" style="display:inline-block;vertical-align:middle;zoom:1.5;" class="md-checkbox" name="assurance_checkboxes" value=26>'
                        +"<span title='Note: This relates to opinion provided by the expert'>The expert has set out any <b>assumptions</b> made <span style='color: blue'>(hover over for more info)</span></label>"
                        +'</input>'
                        +'</div>'
                        +'<div class="md-layout-item md-size-100" style="text-align: left">'
                        +'<input type="checkbox" style="display:inline-block;vertical-align:middle;zoom:1.5;" class="md-checkbox" name="assurance_checkboxes" value=27>'
                        +"<span title='Note: This relates to the details of apportioning injuries'>The expert has set out any <b>calculations</b> made <span style='color: blue'>(hover over for more info)</span></label>"
                        +'</input>'
                        +'</div>'
                        +'<div class="md-layout-item md-size-100" style="text-align: left">'
                        +'<input type="checkbox" style="display:inline-block;vertical-align:middle;zoom:1.5;" class="md-checkbox" name="assurance_checkboxes" value=8>'
                        +"<span title='Note: Documents include GP records, Hospital records, Rehab records, X-ray records'>The report lists details of <b>all key documents</b> or other evidence which the expert has been provided with <span style='color: blue'>(hover over for more info)</span></label>"
                        +'</input>'
                        +'</div>'
                        +'<div class="md-layout-item md-size-100" style="text-align: left">'
                        +'<input type="checkbox" style="display:inline-block;vertical-align:middle;zoom:1.5;" class="md-checkbox" name="assurance_checkboxes" value=28>'
                        +"<label>The <b>language</b> of the report does not advocate for the instructing party</label>"
                        +'</input>'
                        +'</div>'
                        +'<div class="md-layout-item md-size-100" style="text-align: left">'
                        +'<input type="checkbox" style="display:inline-block;vertical-align:middle;zoom:1.5;" class="md-checkbox" name="assurance_checkboxes" value=2>'
                        +"<label>The expert has listed the <b>purpose</b> of the report</label>"
                        +'</input>'
                        +'</div>'
                        +'<div class="md-layout-item md-size-100" style="text-align: left">'
                        +'<input type="checkbox" style="display:inline-block;vertical-align:middle;zoom:1.5;" class="md-checkbox" name="assurance_checkboxes" value=1>'
                        +"<label>The expert has listed their <b>qualifications</b></label>"
                        +'</input>'
                        +'</div>'
                        +'<div class="md-layout-item md-size-100" style="text-align: left">'
                        +'<input type="checkbox" style="display:inline-block;vertical-align:middle;zoom:1.5;" class="md-checkbox" name="assurance_checkboxes" value=9>'
                        +"<label>The report follows a <b>chronological order</b></label>"
                        +'</input>'
                        +'</div>'
                        +'<div class="md-layout-item md-size-100" style="text-align: left">'
                        +'<input type="checkbox" style="display:inline-block;vertical-align:middle;zoom:1.5;" class="md-checkbox" name="assurance_checkboxes" value=13>'
                        +"<span title='Note: The expert’s report must be succinct, focused and analytical. But they must also be evidence-based.'>The overall <b>style</b>, <b>size</b> and <b>tone</b> of report is more focused on analysis and opinion than history and narrative <span style='color: blue'>(hover over for more info)</span></label>"
                        +'</input>'
                        +'</div>'
                        +'<div class="md-layout-item md-size-100" style="text-align: left">'
                        +'<input type="checkbox" style="display:inline-block;vertical-align:middle;zoom:1.5;" class="md-checkbox" name="assurance_checkboxes" value=15>'
                        +"<label>The report includes a <b>declaration to the court</b></label>"
                        +'</input>'
                        +'</div>'
                        +'<div class="md-layout-item md-size-100" style="text-align: left">'
                        +'<input type="checkbox" style="display:inline-block;vertical-align:middle;zoom:1.5;" class="md-checkbox" name="assurance_checkboxes" value=16>'
                        +"<label>The expert has provided an opinion within the scope of their <b>competence</b></label>"
                        +'</input>'
                        +'</div>'
                        +'<div class="md-layout-item md-size-100" style="text-align: left">'
                        +'<input type="checkbox" style="display:inline-block;vertical-align:middle;zoom:1.5;" class="md-checkbox" name="assurance_checkboxes" value=17>'
                        +"<label>The expert has not identified <b>unfamiliarity</b> with the instruction</label>"
                        +'</input>'
                        +'</div>'
                        +'<style>'
                        + 'input[type="checkbox"]{'
                        + '    -webkit-appearance: initial;'
                        + '    appearance: initial;'
                        + '    background: gray;'
                        + '    width: 20px;'
                        + '    height: 20px;'
                        + '    border: none;'
                        + '    position: relative;'
                        + '}'
                        + 'input[type="checkbox"]:checked {'
                        + '    background: red;'
                        + '}'
                        + 'input[type="checkbox"]:checked:after {'
                        + '    /* Heres your symbol replacement */'
                        + '    content: "X";'
                        + '    color: #fff;'
                        + '    /* The following positions my tick in the center, '
                        + '     * but you could just overlay the entire box'
                        + '     * with a full after element with a background if you want to */'
                        + '    position: absolute;'
                        + '    left: 50%;'
                        + '    top: 50%;'
                        + '    -webkit-transform: translate(-50%,-50%);'
                        + '    -moz-transform: translate(-50%,-50%);'
                        + '    -ms-transform: translate(-50%,-50%);'
                        + '    transform: translate(-50%,-50%);'
                        + '    /*'
                        + '     * If you want to fully change the check appearance, use the following:'
                        + '     * content: " ";'
                        + '     * width: 100%;'
                        + '     * height: 100%;'
                        + '     * background: blue;'
                        + '     * top: 0;'
                        + '     * left: 0;'
                        + '     */'
                        + '}'
                        + '</style>',
                        showCancelButton: true,
                        showCloseButton: true,
                        confirmButtonClass: "md-button md-success",
                        confirmButtonText: "Proceed",
                        cancelButtonClass: "md-button md-danger",
                        buttonsStyling: true,
                        preConfirm: () => {
                            document.getElementsByName('assurance_checkboxes').forEach(element => {
                            if (element.checked){
                                quality_assurance_form_integer_results.push(element.value)
                                console.log(quality_assurance_form_integer_results)
                                var listItem = document.createElement('li');
                                listItem.innerHTML = quality_assurance_dictionary[element.value];
                                listElement.appendChild(listItem);
                            }
                            });
                        }
                    },
                    {
                        title: 'The following failed the Non-Clinical Quality Assurance check!',
                        width: 1200,
                        animation: false,
                        html: listContainer,
                        showCancelButton: true,
                        showCloseButton: true,
                        confirmButtonClass: "md-button md-success",
                        cancelButtonClass: "md-button md-danger",
                        confirmButtonText: 'Next',
                        buttonsStyling: true,
                    },
                    {
                title: "Clinical Quality of Reports<br>Is the amendment request related to any one of these reasons?",
                width: 1200,
                animation: false,
                html:   '<ul>'
                        +'<div class="md-layout-item md-size-100" style="text-align: left">'
                            +'<li><span style="font-size: 32px"><u>Injury</u></span>'
                                +'<ul>'
                                    +'<li>'
                                        +'<input type="checkbox" style="display:inline-block;vertical-align:middle;zoom:1.5;" class="md-checkbox" name="clinical_assurance_checkboxes" value=1>'
                                        +"<label style='font-size: 27px' title='e.g. not mentioned, unclear or vague'>Onset of injury <span style='color: blue'>(hover over for more info)</span></label>"
                                        +'</input>'
                                    +'</li>'
                                    +'<li>'
                                        +'<input type="checkbox" style="display:inline-block;vertical-align:middle;zoom:1.5;" class="md-checkbox" name="clinical_assurance_checkboxes" value=2>'
                                        +"<label style='font-size: 27px' title='e.g. proposed injury not in report'>Missed injury <span style='color: blue'>(hover over for more info)</span></label>"
                                        +'</input>'
                                    +'</li>'
                                    +'<li>'
                                        +'<input type="checkbox" style="display:inline-block;vertical-align:middle;zoom:1.5;" class="md-checkbox" name="clinical_assurance_checkboxes" value=3>'
                                        +"<label style='font-size: 27px' title='e.g. accident mechanism missing from report'>Mechanism of injury <span style='color: blue'>(hover over for more info)</span></label>"
                                        +'</input>'
                                    +'</li>'
                                    +'<li>'
                                        +'<input type="checkbox" style="display:inline-block;vertical-align:middle;zoom:1.5;" class="md-checkbox" name="clinical_assurance_checkboxes" value=4>'
                                        +"<label style='font-size: 27px' title='expert has reported no injury. However IP have advised there is'>No injury at all in report <span style='color: blue'>(hover over for more info)</span></label>"
                                        +'</input>'
                                    +'</li>'
                                +'</ul>'
                            +'</li>'
                            +'<li><span style="font-size: 32px"><u>Claimant medical background</u></span>'
                                +'<ul>'
                                    +'<li>'
                                        +'<input type="checkbox" style="display:inline-block;vertical-align:middle;zoom:1.5;" class="md-checkbox" name="clinical_assurance_checkboxes" value=5>'
                                        +"<label style='font-size: 27px' title='(Relevance of health factors to the accident are unclear e.g. expert failed to record how medical condition is affected by accident or not; expert failed to apportion injury based on medical background'>Past medical/accident history <span style='color: blue'>(hover over for more info)</span></label>"
                                        +'</input>'
                                    +'</li>'
                                +'</ul>'
                            +'</li>'
                            +'<li><span style="font-size: 32px"><u>Examination</u></span>'
                                +'<ul>'
                                    +'<li>'
                                        +'<input type="checkbox" style="display:inline-block;vertical-align:middle;zoom:1.5;" class="md-checkbox" name="clinical_assurance_checkboxes" value=6>'
                                        +"<label style='font-size: 27px' title='e.g. physical examination normal but psychological examination present)'>Inconsistent findings <span style='color: blue'>(hover over for more info)</span></label>"
                                        +'</input>'
                                    +'</li>'
                                    +'<li>'
                                        +'<input type="checkbox" style="display:inline-block;vertical-align:middle;zoom:1.5;" class="md-checkbox" name="clinical_assurance_checkboxes" value=7>'
                                        +"<label style='font-size: 27px' title='e.g. details are insufficient, cursory or no examination results present'>Physical examination <span style='color: blue'>(hover over for more info)</span></label>"
                                        +'</input>'
                                    +'</li>'
                                +'</ul>'
                            +'</li>'
                            +'<li><span style="font-size: 32px"><u>Prognosis</u></span>'
                                +'<ul>'
                                    +'<li>'
                                        +'<input type="checkbox" style="display:inline-block;vertical-align:middle;zoom:1.5;" class="md-checkbox" name="clinical_assurance_checkboxes" value=8>'
                                        +"<label style='font-size: 27px' title='e.g. queried or increase/decrease request'>Prognosis/recovery timeframe <span style='color: blue'>(hover over for more info)</span></label>"
                                        +'</input>'
                                    +'</li>'
                                +'</ul>'
                            +'</li>'
                            +'<li><span style="font-size: 32px"><u>Treatment</u></span>'
                                +'<ul>'
                                    +'<li>'
                                        +'<input type="checkbox" style="display:inline-block;vertical-align:middle;zoom:1.5;" class="md-checkbox" name="clinical_assurance_checkboxes" value=9>'
                                        +"<label style='font-size: 27px' title='e.g. treatment suggested by expert inappropriate/not required; treatment suggested not advised by expert'>Treatment <span style='color: blue'>(hover over for more info)</span></label>"
                                        +'</input>'
                                    +'</li>'
                                +'</ul>'
                            +'</li>'
                            +'<li><span style="font-size: 32px"><u>Opinion</u></span>'
                                +'<ul>'
                                    +'<li>'
                                        +'<input type="checkbox" style="display:inline-block;vertical-align:middle;zoom:1.5;" class="md-checkbox" name="clinical_assurance_checkboxes" value=10>'
                                        +"<label style='font-size: 27px'>Opinion and prognosis are not provided for all injuries relevant to the accident</label>"
                                        +'</input>'
                                    +'</li>'
                                    +'<li>'
                                        +'<input type="checkbox" style="display:inline-block;vertical-align:middle;zoom:1.5;" class="md-checkbox" name="clinical_assurance_checkboxes" value=11>'
                                        +"<label style='font-size: 27px'>Report omits facts that do not support the expert’s opinion</label>"
                                        +'</input>'
                                    +'</li>'
                                    +'<li>'
                                        +'<input type="checkbox" style="display:inline-block;vertical-align:middle;zoom:1.5;" class="md-checkbox" name="clinical_assurance_checkboxes" value=12>'
                                        +"<label style='font-size: 27px'>Clinical opinion not based on claimant’s account</label>"
                                        +'</input>'
                                    +'</li>'
                                    +'<li>'
                                        +'<input type="checkbox" style="display:inline-block;vertical-align:middle;zoom:1.5;" class="md-checkbox" name="clinical_assurance_checkboxes" value=13>'
                                        +"<label style='font-size: 27px' title='e.g one or more injuries are non-soft tissue and require another expert type'>Injury falls outside expert's scope of expertise <span style='color: blue'>(hover over for more info)</span></label>"
                                        +'</input>'
                                    +'</li>'
                                +'</ul>'
                            +'</li>'
                            +'<li><span style="font-size: 32px"><u>Recommendations</u></span>'
                                +'<ul>'
                                    +'<li>'
                                        +'<input type="checkbox" style="display:inline-block;vertical-align:middle;zoom:1.5;" class="md-checkbox" name="clinical_assurance_checkboxes" value=14>'
                                        +"<label style='font-size: 27px' title='e.g. specialist referral challenged or requested'>Referral to specialist <span style='color: blue'>(hover over for more info)</span></label>"
                                        +'</input>'
                                    +'</li>'
                                    +'<li>'
                                        +'<input type="checkbox" style="display:inline-block;vertical-align:middle;zoom:1.5;" class="md-checkbox" name="clinical_assurance_checkboxes" value=15>'
                                        +"<label style='font-size: 27px' title='e.g. investigation challenged or requested'>Referral for investigations <span style='color: blue'>(hover over for more info)</span></label>"
                                        +'</input>'
                                    +'</li>'
                                +'</ul>'
                            +'</li>'
                            +'<li><span style="font-size: 32px"><u>Report quality</u></span>'
                                +'<ul>'
                                    +'<li>'
                                        +'<input type="checkbox" style="display:inline-block;vertical-align:middle;zoom:1.5;" class="md-checkbox" name="clinical_assurance_checkboxes" value=16>'
                                        +"<label style='font-size: 27px' title='e.g. significant copying and pasting, prognosis is standard, broad vague and nonspecific timescales and explanation given by expert'>Factory produced <span style='color: blue'>(hover over for more info)</span></label>"
                                        +'</input>'
                                    +'</li>'
                                    +'<li>'
                                        +'<input type="checkbox" style="display:inline-block;vertical-align:middle;zoom:1.5;" class="md-checkbox" name="clinical_assurance_checkboxes" value=17>'
                                        +"<label style='font-size: 27px'>Language offensive, derogatory or misrepresented</label>"
                                        +'</input>'
                                    +'</li>'
                                +'</ul>'
                            +'</li>'
                            +'<li><span style="font-size: 32px"><u>Consultation</u></span>'
                                +'<ul>'
                                    +'<li>'
                                        +'<input type="checkbox" style="display:inline-block;vertical-align:middle;zoom:1.5;" class="md-checkbox" name="clinical_assurance_checkboxes" value=18>'
                                        +"<label style='font-size: 27px' title='e.g. consulting time queried'>Sufficient time spent with claimant <span style='color: blue'>(hover over for more info)</span></label>"
                                        +'</input>'
                                    +'</li>'
                                +'</ul>'
                            +'</li>'
                            +'<li><span style="font-size: 32px"><u>Medical records</u></span>'
                                +'<ul>'
                                    +'<li>'
                                        +'<input type="checkbox" style="display:inline-block;vertical-align:middle;zoom:1.5;" class="md-checkbox" name="clinical_assurance_checkboxes" value=19>'
                                        +"<label style='font-size: 27px' title='e.g. records were required to finalise report'>Records review required <span style='color: blue'>(hover over for more info)</span></label>"
                                        +'</input>'
                                    +'</li>'
                                    +'<li>'
                                        +'<input type="checkbox" style="display:inline-block;vertical-align:middle;zoom:1.5;" class="md-checkbox" name="clinical_assurance_checkboxes" value=20>'
                                        +"<label style='font-size: 27px' title='queried by IP'>Expert has requested records <span style='color: blue'>(hover over for more info)</span></label>"
                                        +'</input>'
                                    +'</li>'
                                +'</ul>'
                            +'</li>'
                        +'</div>'
                        +'</ul>'
                        +'<style>'
                        + 'input[type="checkbox"]{'
                        + '    -webkit-appearance: initial;'
                        + '    appearance: initial;'
                        + '    background: gray;'
                        + '    width: 20px;'
                        + '    height: 20px;'
                        + '    border: none;'
                        + '    position: relative;'
                        + '}'
                        + 'input[type="checkbox"]:checked {'
                        + '    background: green;'
                        + '}'
                        + 'input[type="checkbox"]:checked:after {'
                        + '    /* Heres your symbol replacement */'
                        + '    content: "✓";'
                        + '    color: #fff;'
                        + '    /* The following positions my tick in the center, '
                        + '     * but you could just overlay the entire box'
                        + '     * with a full after element with a background if you want to */'
                        + '    position: absolute;'
                        + '    left: 50%;'
                        + '    top: 50%;'
                        + '    -webkit-transform: translate(-50%,-50%);'
                        + '    -moz-transform: translate(-50%,-50%);'
                        + '    -ms-transform: translate(-50%,-50%);'
                        + '    transform: translate(-50%,-50%);'
                        + '    /*'
                        + '     * If you want to fully change the check appearance, use the following:'
                        + '     * content: " ";'
                        + '     * width: 100%;'
                        + '     * height: 100%;'
                        + '     * background: blue;'
                        + '     * top: 0;'
                        + '     * left: 0;'
                        + '     */'
                        + '}'
                        + '</style>',
                        showCancelButton: true,
                        showCloseButton: true,
                        confirmButtonClass: "md-button md-success",
                        confirmButtonText: "Finish",
                        cancelButtonClass: "md-button md-danger",
                        buttonsStyling: true,
                        preConfirm: () => {
                            document.getElementsByName('clinical_assurance_checkboxes').forEach(element => {
                            if (element.checked){
                                clinical_quality_assurance_form_integer_results.push(element.value)
                                console.log(clinical_quality_assurance_form_integer_results)
                                var listItem = document.createElement('li');
                                listItem.innerHTML = quality_assurance_dictionary[element.value];
                                listElement.appendChild(listItem);
                            }
                            });
                        }
                    }
                    ]).then(result => {
                        if (result.value) {
                            if (quality_assurance_form_integer_results.length){
                                amroc_status = false
                                failed_checks = quality_assurance_form_integer_results
                                var clinical_quality_checks = clinical_quality_assurance_form_integer_results;
                                for (var item in this.outputData.inputItems) {
                                    if (this.outputData.inputItems[item].selected) {
                                        this.outputData.inputItems[item].visible = true
                                    } else {
                                        this.outputData.inputItems[item].visible = false
                                    }
                                }
                                for (var index in this.outputData.inputItems) {
                                    if (this.outputData.inputItems[index].selected){
                                        this.selected_documents.push({'id': this.outputData.inputItems[index].id, 'name': this.outputData.inputItems[index].name, 'type': this.outputData.inputItems[index].type})
                                    }
                                }
                                console.log('CALLING HERE FOR EMAIL WITH failed_checks = ', failed_checks)
                                this.email_template(null, false, amroc_status, failed_checks, clinical_quality_checks)
                            }else{
                                amroc_status = true
                                failed_checks = ''
                                var clinical_quality_checks = clinical_quality_assurance_form_integer_results;
                                for (var item in this.outputData.inputItems) {
                                    if (this.outputData.inputItems[item].selected) {
                                        this.outputData.inputItems[item].visible = true
                                    } else {
                                        this.outputData.inputItems[item].visible = false
                                    }
                                }
                                for (var index in this.outputData.inputItems) {
                                    if (this.outputData.inputItems[index].selected){
                                        this.selected_documents.push({'id': this.outputData.inputItems[index].id, 'name': this.outputData.inputItems[index].name, 'type': this.outputData.inputItems[index].type})
                                    }
                                }
                                this.email_template(null, false, amroc_status, failed_checks, clinical_quality_checks)
                            }
                        }
                        return
                    })
          }
      },
      amroc_check:function(){
        var claimant_address = []
            if (this.currentCase.claimant.address1){
              claimant_address.push(this.currentCase.claimant.address1)
            }
            if (this.currentCase.claimant.address2){
              claimant_address.push(this.currentCase.claimant.address2)
            }
            if (this.currentCase.claimant.address3){
              claimant_address.push(this.currentCase.claimant.address3)
            }
            if (this.currentCase.claimant.postcode){
              claimant_address.push(this.currentCase.claimant.postcode)
            }
        var listContainer = document.createElement('div');
        var listElement = document.createElement('ul');


        var quality_assurance_html = ''
        listContainer.appendChild(listElement);


        var quality_assurance_form_integer_results = []
        var quality_assurance_dictionary =
        {
          '1': "The expert has listed their qualifications",
          '2': "The expert has listed the purpose of the report",
          '3': "The report contains Claimant's correct Title",
          '4': "The report contains Claimant's correct First name",
          '5': "The report contains Claimant's correct Last name",
          '6': "The report contains Claimant's correct Date of Birth (DOB)",
          '7': "The report contains Claimant's correct Date of Accident (DOA)",
          '8': "The report lists details of all key documents or other evidence which the expert has been provided with",
          '9': "The report follows a chronological order",
          '10': "The report has the matters of fact and opinion clearly distinguished and these are kept separate",
          '11': "The expert clearly states the source of Statements of Fact that are relied upon",
          '12': "The report is non-provisional",
          '13': "The overall style, size and tone of report is more focused on analysis and opinion than history and narrative",
          '14': "Part 35 of the Civil Procedure Rules and the Practice Direction is included",
          '15': "The report includes a declaration to the court",
          '16': "The expert has provided an opinion within the scope of their competence",
          '17': "The expert has not identified unfamiliarity with the instruction",
          '18': "The expert has checked and stated the claimant's photo identification and type",
          '19': "The report contains Claimant's correct Address",
          '20': "The report contains Claimant's correct MedCo Reference",
          '21': "The report contains Claimant's correct Instructing Party Reference",
          '22': "The report contains Claimant's correct Precise examination location",
          '23': "The claimant's Gender throughout the report is correct",
          '24': "The expert has provided a description of the claimant's occupation",
          '25': "There was no third party present or there was a third party noted in attendance and the expert states the name of the individual attending and employer (if applicable)",
          '26': "The expert has set out any assumptions made",
          '27': "The expert has set out any calculations made",
          '28': "The language of the report does not advocate for the instructing party",
        }
        Swal.mixin({
            confirmButtonText: 'Next &rarr;',
            showCancelButton: true,
            progressSteps: ['1', '2']
        }).queue([
            {
            // title: "Quality assurance (Protocol C)<br>Check only the ones that are failing!",
            width: 1200,
            animation: false,
            html:   '<div class="md-layout-item md-size-100" style="text-align: left">'
                    // +'<input type="checkbox" style="display:inline-block;vertical-align:middle;zoom:1.5;" class="md-checkbox" name="assurance_checkboxes" value=3>'
                    // +"<label>The report contains Claimant's correct <b>Title</b> [" + this.currentCase.claimant.title + "]</label>"
                    // +'</input>'
                    // +'</div>'
                    // +'<div class="md-layout-item md-size-100" style="text-align: left">'
                    +'<input type="checkbox" style="display:inline-block;vertical-align:middle;zoom:1.5;" class="md-checkbox" name="assurance_checkboxes" value=4>'
                    +"<label>The report contains Claimant's correct <b>First name</b> [" + this.currentCase.claimant.first_name + "]</label>"
                    +'</input>'
                    +'</div>'
                    +'<div class="md-layout-item md-size-100" style="text-align: left">'
                    +'<input type="checkbox" style="display:inline-block;vertical-align:middle;zoom:1.5;" class="md-checkbox" name="assurance_checkboxes" value=5>'
                    +"<label>The report contains Claimant's correct <b>Last Name</b> [" + this.currentCase.claimant.last_name + "]</label>"
                    +'</input>'
                    +'</div>'
                    +'<div class="md-layout-item md-size-100" style="text-align: left">'
                    +'<input type="checkbox" style="display:inline-block;vertical-align:middle;zoom:1.5;" class="md-checkbox" name="assurance_checkboxes" value=19>'
                    +"<label>The report contains Claimant's correct <b>Address</b> [" + claimant_address.join(', ') + "]</label>"
                    +'</input>'
                    +'</div>'
                    +'<div class="md-layout-item md-size-100" style="text-align: left">'
                    +'<input type="checkbox" style="display:inline-block;vertical-align:middle;zoom:1.5;" class="md-checkbox" name="assurance_checkboxes" value=6>'
                    +"<label>The report contains Claimant's correct <b>Date of Birth(DOB)</b> [" + moment(this.currentCase.claimant.date_of_birth).format('DD/MM/YYYY') + "]</label>"
                    +'</input>'
                    +'</div>'
                    +'<div class="md-layout-item md-size-100" style="text-align: left">'
                    +'<input type="checkbox" style="display:inline-block;vertical-align:middle;zoom:1.5;" class="md-checkbox" name="assurance_checkboxes" value=7>'
                    +"<label>The report contains Claimant's correct <b>Date of Accident(DOA)</b> [" + moment(this.currentCase.accident.date).format('DD/MM/YYYY') + "]</label>"
                    +'</input>'
                    +'</div>'
                    +'<div class="md-layout-item md-size-100" style="text-align: left">'
                    +'<input type="checkbox" style="display:inline-block;vertical-align:middle;zoom:1.5;" class="md-checkbox" name="assurance_checkboxes" value=20>'
                    +"<label>The report contains Claimant's correct <b>MedCo reference</b> [" + this.currentCase.instructing_party.medco_id + "]</label>"
                    +'</input>'
                    +'</div>'
                    +'<div class="md-layout-item md-size-100" style="text-align: left">'
                    +'<input type="checkbox" style="display:inline-block;vertical-align:middle;zoom:1.5;" class="md-checkbox" name="assurance_checkboxes" value=21>'
                    +"<label>The report contains Claimant's correct <b>Instructing Party reference</b> [" + this.currentCase.instructing_party.instruction_party_reference + "]</label>"
                    +'</input>'
                    +'</div>'
                    +'<div class="md-layout-item md-size-100" style="text-align: left">'
                    +'<input type="checkbox" style="display:inline-block;vertical-align:middle;zoom:1.5;" class="md-checkbox" name="assurance_checkboxes" value=22>'
                    +"<label>The report contains Claimant's correct <b>Precise examination location</b></label>"
                    +'</input>'
                    +'</div>'
                    +'<div class="md-layout-item md-size-100" style="text-align: left">'
                    +'<input type="checkbox" style="display:inline-block;vertical-align:middle;zoom:1.5;" class="md-checkbox" name="assurance_checkboxes" value=23>'
                    +"<label>The claimant's <b>Gender</b> throughout the report is correct [" + this.currentCase.claimant.gender + "]</label>"
                    +'</input>'
                    +'</div>'
                    +'<div class="md-layout-item md-size-100" style="text-align: left">'
                    +'<input type="checkbox" style="display:inline-block;vertical-align:middle;zoom:1.5;" class="md-checkbox" name="assurance_checkboxes" value=18>'
                    +"<span title='Note: Photo Id can include: Passport, Driving licence, National identity card, PCO licence card'>The expert has checked and stated the claimant's <b>photo identification</b> and type <span style='color: blue'>(hover over for more info)</span></label>"
                    +'</input>'
                    +'</div>'
                    +'<div class="md-layout-item md-size-100" style="text-align: left">'
                    +'<input type="checkbox" style="display:inline-block;vertical-align:middle;zoom:1.5;" class="md-checkbox" name="assurance_checkboxes" value=24>'
                    +"<span title='Note: This should not be vague e.g. “worker”'>The expert has provided a description of the claimant's <b>occupation</b> <span style='color: blue'>(hover over for more info)</span></label>"
                    +'</input>'
                    +'</div>'
                    +'<div class="md-layout-item md-size-100" style="text-align: left">'
                    +'<input type="checkbox" style="display:inline-block;vertical-align:middle;zoom:1.5;" class="md-checkbox" name="assurance_checkboxes" value=10>'
                    +"<label>The report has the <b>matters of fact</b> and <b>opinion</b> clearly distinguished and these are kept separate</label>"
                    +'</input>'
                    +'</div>'
                    +'<div class="md-layout-item md-size-100" style="text-align: left">'
                    +'<input type="checkbox" style="display:inline-block;vertical-align:middle;zoom:1.5;" class="md-checkbox" name="assurance_checkboxes" value=14>'
                    +"<label><b>Part 35 of the Civil Procedure Rules</b> <a href='https://www.justice.gov.uk/courts/procedure-rules/civil/rules/part35' target='_blank'>(URL)</a> and the <b>Practice Direction</b> <a href='https://www.justice.gov.uk/courts/procedure-rules/civil/rules/part35/pd_part35' target='_blank'>(URL)</a> is included</label>"
                    +'</input>'
                    +'</div>'
                    +'<div class="md-layout-item md-size-100" style="text-align: left">'
                    +'<input type="checkbox" style="display:inline-block;vertical-align:middle;zoom:1.5;" class="md-checkbox" name="assurance_checkboxes" value=11>'
                    +"<label>The expert clearly states the source of <b>Statements of Fact</b> that are relied upon</label>"
                    +'</input>'
                    +'</div>'
                    +'<div class="md-layout-item md-size-100" style="text-align: left">'
                    +'<input type="checkbox" style="display:inline-block;vertical-align:middle;zoom:1.5;" class="md-checkbox" name="assurance_checkboxes" value=12>'
                    +"<label>The report is <b>non-provisional</b></label>"
                    +'</input>'
                    +'</div>'
                    +'<div class="md-layout-item md-size-100" style="text-align: left">'
                    +'<input type="checkbox" style="display:inline-block;vertical-align:middle;zoom:1.5;" class="md-checkbox" name="assurance_checkboxes" value=25>'
                    +"<span title='Note: The third party would be a translator or McKenzie friend. The name of the employer should only be required if the employment firm is featured on the claim.'>There was no <b>third party</b> present or there was a third party noted in attendance and the expert states the name of the individual attending and employer (<b>if applicable</b>) <span style='color: blue'>(hover over for more info)</span></label>"
                    +'</input>'
                    +'</div>'
                    +'<div class="md-layout-item md-size-100" style="text-align: left">'
                    +'<input type="checkbox" style="display:inline-block;vertical-align:middle;zoom:1.5;" class="md-checkbox" name="assurance_checkboxes" value=26>'
                    +"<span title='Note: This relates to opinion provided by the expert'>The expert has set out any <b>assumptions</b> made <span style='color: blue'>(hover over for more info)</span></label>"
                    +'</input>'
                    +'</div>'
                    +'<div class="md-layout-item md-size-100" style="text-align: left">'
                    +'<input type="checkbox" style="display:inline-block;vertical-align:middle;zoom:1.5;" class="md-checkbox" name="assurance_checkboxes" value=27>'
                    +"<span title='Note: This relates to the details of apportioning injuries'>The expert has set out any <b>calculations</b> made <span style='color: blue'>(hover over for more info)</span></label>"
                    +'</input>'
                    +'</div>'
                    +'<div class="md-layout-item md-size-100" style="text-align: left">'
                    +'<input type="checkbox" style="display:inline-block;vertical-align:middle;zoom:1.5;" class="md-checkbox" name="assurance_checkboxes" value=8>'
                    +"<span title='Note: Documents include GP records, Hospital records, Rehab records, X-ray records'>The report lists details of <b>all key documents</b> or other evidence which the expert has been provided with <span style='color: blue'>(hover over for more info)</span></label>"
                    +'</input>'
                    +'</div>'
                    +'<div class="md-layout-item md-size-100" style="text-align: left">'
                    +'<input type="checkbox" style="display:inline-block;vertical-align:middle;zoom:1.5;" class="md-checkbox" name="assurance_checkboxes" value=28>'
                    +"<label>The <b>language</b> of the report does not advocate for the instructing party</label>"
                    +'</input>'
                    +'</div>'
                    +'<div class="md-layout-item md-size-100" style="text-align: left">'
                    +'<input type="checkbox" style="display:inline-block;vertical-align:middle;zoom:1.5;" class="md-checkbox" name="assurance_checkboxes" value=2>'
                    +"<label>The expert has listed the <b>purpose</b> of the report</label>"
                    +'</input>'
                    +'</div>'
                    +'<div class="md-layout-item md-size-100" style="text-align: left">'
                    +'<input type="checkbox" style="display:inline-block;vertical-align:middle;zoom:1.5;" class="md-checkbox" name="assurance_checkboxes" value=1>'
                    +"<label>The expert has listed their <b>qualifications</b></label>"
                    +'</input>'
                    +'</div>'
                    +'<div class="md-layout-item md-size-100" style="text-align: left">'
                    +'<input type="checkbox" style="display:inline-block;vertical-align:middle;zoom:1.5;" class="md-checkbox" name="assurance_checkboxes" value=9>'
                    +"<label>The report follows a <b>chronological order</b></label>"
                    +'</input>'
                    +'</div>'
                    +'<div class="md-layout-item md-size-100" style="text-align: left">'
                    +'<input type="checkbox" style="display:inline-block;vertical-align:middle;zoom:1.5;" class="md-checkbox" name="assurance_checkboxes" value=13>'
                    +"<span title='Note: The expert’s report must be succinct, focused and analytical. But they must also be evidence-based.'>The overall <b>style</b>, <b>size</b> and <b>tone</b> of report is more focused on analysis and opinion than history and narrative <span style='color: blue'>(hover over for more info)</span></label>"
                    +'</input>'
                    +'</div>'
                    +'<div class="md-layout-item md-size-100" style="text-align: left">'
                    +'<input type="checkbox" style="display:inline-block;vertical-align:middle;zoom:1.5;" class="md-checkbox" name="assurance_checkboxes" value=15>'
                    +"<label>The report includes a <b>declaration to the court</b></label>"
                    +'</input>'
                    +'</div>'
                    +'<div class="md-layout-item md-size-100" style="text-align: left">'
                    +'<input type="checkbox" style="display:inline-block;vertical-align:middle;zoom:1.5;" class="md-checkbox" name="assurance_checkboxes" value=16>'
                    +"<label>The expert has provided an opinion within the scope of their <b>competence</b></label>"
                    +'</input>'
                    +'</div>'
                    +'<div class="md-layout-item md-size-100" style="text-align: left">'
                    +'<input type="checkbox" style="display:inline-block;vertical-align:middle;zoom:1.5;" class="md-checkbox" name="assurance_checkboxes" value=17>'
                    +"<label>The expert has not identified <b>unfamiliarity</b> with the instruction</label>"
                    +'</input>'
                    +'</div>',
                    showCancelButton: true,
                    showCloseButton: true,
                    confirmButtonClass: "md-button md-success",
                    confirmButtonText: "Proceed",
                    cancelButtonClass: "md-button md-danger",
                    buttonsStyling: true,
                    preConfirm: () => {
                        document.getElementsByName('assurance_checkboxes').forEach(element => {
                        if (element.checked){
                            quality_assurance_form_integer_results.push(element.value)
                            console.log(quality_assurance_form_integer_results)
                            var listItem = document.createElement('li');
                            listItem.innerHTML = quality_assurance_dictionary[element.value];
                            listElement.appendChild(listItem);
                        }
                        });
                    }
                },
                {
                    title: 'The following failed the quality assurance check!',
                    width: 1200,
                    animation: false,
                    html: listContainer,
                    showCancelButton: true,
                    showCloseButton: true,
                    confirmButtonClass: "md-button md-success",
                    cancelButtonClass: "md-button md-danger",
                    confirmButtonText: 'SAVE',
                    buttonsStyling: true,
                }
                ]).then(result => {
                    if (result.value) {
                        if (quality_assurance_form_integer_results.length){
                            return {amroc_status:false, failed_checks:quality_assurance_form_integer_results}
                        }else{
                            return {amroc_status:true, failed_checks:null}
                        }
                    }
                    return
                })
      },
  },
  created() {
    var product = this.currentAppointment.product_name.toLowerCase()
    if (product.includes('medco') && !product.includes('non')){
        this.request_types_filtered = this.request_types.filter( x  => {
            return x.type.toLowerCase().includes(product) && !x.type.toLowerCase().includes('non');
        })
    }else{
        this.request_types_filtered = this.request_types.filter( x  => {
            return x.type.toLowerCase().includes(product);
        })

    }

      this.$http
        .get(this.url__case_verbose+this.id+'/')
        .then(response => {
            this.objectData = response.data;
            for (var i in response.data.attachments) {
                if (response.data.attachments[i].file) {
                    this.all_attachments.push(response.data.attachments[i])
                }
            }
            this.$http
                .get(this.url__appointment_medical_reports+this.appointmentData.id+'/')
                .then(response => {
                    console.log(response.data)
                    for (var i in response.data) {
                        console.log(response.data[i])
                        this.all_attachments.push(response.data[i])
                    }
                    console.log(this.all_attachments)
                    const inputData_local = this.all_attachments
                    const list_of_documents = []
                    for(var item in inputData_local){
                        var parsed_datetime_created = null
                        if (inputData_local[item].datetime){
                            parsed_datetime_created = moment(inputData_local[item].datetime).format('DD/MM/YYYY HH:mm')
                        }else{
                            parsed_datetime_created = moment(inputData_local[item].date_created).format('DD/MM/YYYY HH:mm')
                        }
                        var url_split_list = inputData_local[item].file.split('/')
                        var computed_filename = url_split_list[url_split_list.length - 1]
                        this.outputData.inputItems.push({ id: inputData_local[item].id,
                                                        type: inputData_local[item].type,
                                                        filename: computed_filename,
                                                        date_created: parsed_datetime_created,
                                                        selected: false,
                                                        visible: true
                                                        })
                    }
                    this.inputData = inputData_local
            })
            .catch(function(error) {
                console.error(error.response);
            });
        })
        .catch(function(error) {
            console.error(error.response);
        });
    // this.parse_failed_checks();
  },
  computed: {
      ...mapGetters([
      'currentCase',
      'currentAppointment',
      'currentInstructingParty',
      'currentAgency',
      'currentAgencyFileHandler',
  ])
  },
  watch: {
      "outputData.filter": function (newData, oldData){
          console.log(newData, oldData)
          if (newData){
            const lcTerm = newData.toLowerCase();
            for(var item in this.outputData.inputItems){
                if ( this.outputData.inputItems[item].name.toLowerCase().includes(lcTerm) ){
                    this.outputData.inputItems[item].visible = true
                } else {
                    this.outputData.inputItems[item].visible = false
                }
            }
          } else {
            //  for(var item in this.outputData.inputItems){
            //     this.outputData.inputItems[item].visible = false
            // }
            for (var item in this.outputData.inputItems) {
                if (this.outputData.inputItems[item].selected) {
                    this.outputData.inputItems[item].visible = true
                } else {
                    this.outputData.inputItems[item].visible = false
                }
            }
          }
      },
    //   selected_request_type: function(newData, oldData){
    //       var local_filtered_request_types = []

    //       if(this.filter_selection && !this.filter_selection === "Part 35"){
    //           for (var index in this.request_types){
    //             var split_request_type = this.request_types[index].split(' ')
    //             if (split_request_type[0] === this.filter_selection){
    //                 console.log(split_request_type[0])
    //                 local_filtered_request_types.push(this.request_types[index])
    //             }
    //           }
    //       }else if (this.filter_selection && this.filter_selection === "Part 35"){
    //           for (var index in this.request_types){
    //             var split_request_type = this.request_types[index].split(' ')
    //             if (split_request_type[0] + ' ' + split_request_type[1]  === this.filter_selection){
    //                 console.log(split_request_type[0])
    //                 local_filtered_request_types.push(this.request_types[index])
    //             }
    //           }
    //       }else{
    //           local_filtered_request_types = this.request_types
    //       }

    //       if (newData.length > 2){
    //         for (var index in local_filtered_request_types){
    //           var split_request_type = local_filtered_request_types[index].split(' ')
    //           for (var word in split_request_type.slice(1, split_request_type.length - 1)){
    //               if (split_request_type[word].toLowerCase().startsWith(newData.toLowerCase()))
    //               this.filtered_request_types.push(this.request_types[index])
    //           }
    //         }
    //       }
    //   }
    filter_selection: function(newData, oldData){
        console.log(newData)
        for (var index in this.request_types){
            if (this.request_types[index].startsWith(newData)){
                this.filtered_request_types.push(this.request_types[index])
            }
        }
    }
  }

};
</script>
<style scoped>
    .attachmentTable table, th, td {
        border: 1px solid black;
        border-collapse: collapse;
        text-align: center;
        padding: 8px;
    }
    .attachmentTable th {
        border: 1px solid black;
        border-collapse: collapse;
        text-align: center;
        padding: 8px;
        background-color: #dddddd;
        color: black;
        font-size: 20px
    }
    a.attachmentTable :hover {
        cursor: pointer;
    }
    .attachmentTable table {
        font-family: arial, sans-serif;
        border-collapse: collapse;
        width: 100%;
    }


    .attachmentTable tr:nth-child(even) {
        background-color: #dddddd;
    }

</style>
<style>
</style>