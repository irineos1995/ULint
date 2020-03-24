<template>
  <div class="md-layout">
    <div class="md-layout-item md-medium-size-50 md-xsmall-size-100 md-size-25">
      <stats-card header-color="green">
        <template slot="header">
          <div class="card-icon">
            <router-link :to="{ name: 'Cases', params: { search_criteria: 'all_cases'}}">
              <img src="./icons/total.png">
            </router-link>
          </div>
          <h3>Total cases</h3>
          <h3 class="title">{{ dashboard_stats.total_cases }}</h3>
        </template>
      </stats-card>
    </div>
    <div class="md-layout-item md-medium-size-50 md-xsmall-size-100 md-size-25">
      <stats-card header-color="">
        <template slot="header">
          <div class="card-icon">
            <router-link :to="{ name: 'Cases', params: { search_criteria: 'all_medco_cases'}}">
              <img src="./icons/medco-purple-logo.svg">
            </router-link>
          </div>
          <h3>Medco cases</h3>
          <h3 class="title">{{ dashboard_stats.medco_cases }}</h3>
        </template>
      </stats-card>
    </div>
    <div class="md-layout-item md-medium-size-50 md-xsmall-size-100 md-size-25">
      <stats-card header-color="rose">
        <template slot="header">
          <div class="card-icon">
            <router-link :to="{ name: 'Cases', params: { search_criteria: 'awaiting_report'}}">
              <img src="./icons/awaiting_report.png">
            </router-link>
          </div>
          <h3>Awaiting Report</h3>
          <h3 class="title">{{ dashboard_stats.awaiting_report_counter }}</h3>
        </template>
      </stats-card>
    </div>
    <div class="md-layout-item md-medium-size-50 md-xsmall-size-100 md-size-25">
      <stats-card header-color="warning">
        <template slot="header">
          <div class="card-icon">
            <router-link :to="{ name: 'Cases', params: { search_criteria: 'awaiting_instruction'}}">
              <img src="./icons/awaiting_instruction.png">
            </router-link>
          </div>
          <h3>Awaiting Instruction</h3>
          <h3 class="title">{{ dashboard_stats.awaiting_instruction_counter }}</h3>
        </template>
      </stats-card>
    </div>
    <md-card>
      <md-card-header>
        <h2>Medco Instructions Received this month</h2>
      </md-card-header>
      <md-card-content>
        <area-chart style="zoom: 117%;" height="500px" :data="medcoCasesLineChart" :key="componentKey3" ytitle="Number of Instructions received" xtitle="Day"></area-chart>
      </md-card-content>
    </md-card>
    <md-card>
      <md-card-header>
        <h2>Instructions Received each month of 2019</h2>
      </md-card-header>
      <md-card-content>
        <pie-chart style="zoom: 117%;" height="500px" :data="lineChart" :key="componentKey" ytitle="Number of Instructions received" xtitle="Month"></pie-chart>
      </md-card-content>
    </md-card>
    <md-card>
      <md-card-header>
        <h2>Number of Instructed Appointments this month for each expert</h2>
      </md-card-header>
      <md-card-content>
        <bar-chart style="zoom: 117%;" height="2000px" :data="barChart" :key="componentKey2" ytitle="Expert Name" xtitle="If you are reading this, it means you have found an Easter egg!"></bar-chart>
      </md-card-content>
    </md-card>
    <!-- <div class="card">
      <div class="card-header">
        <h4 class="card-title">Email Statistics</h4> 
        <p class="card-category">Last Campaign Performance</p>
      </div> 
      <div class="card-body">
        <div id="div_1387693901761" class="ct-chart">
          <svg xmlns:ct="http://gionkunz.github.com/chartist-js/ct" width="100%" height="100%" class="ct-chart-pie" style="width: 100%; height: 100%;">
            <g class="ct-series ct-series-a">
              <path d="M80.147,160.789A47.328,47.328,0,0,0,52.328,75.172L52.328,122.5Z" class="ct-slice-pie" ct:value="40">
              </path>
            </g>
            <g class="ct-series ct-series-b">
              <path d="M24.509,160.789A47.328,47.328,0,0,0,80.28,160.692L52.328,122.5Z" class="ct-slice-pie" ct:value="20"></path>
            </g>
            <g class="ct-series ct-series-c">
              <path d="M52.328,75.172A47.328,47.328,0,0,0,24.643,160.886L52.328,122.5Z" class="ct-slice-pie" ct:value="40">
                </path>
            </g>
            <g>
              <text dx="74.83398584264079" dy="115.1874025315491" text-anchor="middle" class="ct-label">40%</text>
              <text dx="52.328125" dy="146.1640625" text-anchor="middle" class="ct-label">20%</text>
              <text dx="29.822264157359218" dy="115.18740253154908" text-anchor="middle" class="ct-label">40%</text>
            </g>
          </svg>
        </div>
      </div> 
    </div> -->
  </div>
</template>

<script>

import AsyncWorldMap from 'vue-material-dashboard-pro/src/components/WorldMap/AsyncWorldMap.vue'
import {
  StatsCard,
  ChartCard,
  ProductCard,
  AnimatedNumber
} from 'vue-material-dashboard-pro/src/components'

import Notifications from 'vue-material-dashboard-pro/src/components/NotificationPlugin'

import Vue from "vue";
// import * as Sentry from '@sentry/browser';
// import * as Integrations from '@sentry/integrations';

import Chartkick from 'vue-chartkick'
import Highcharts from 'highcharts'
import Chart from 'chart.js'
Vue.use(Chartkick.use(Chart))

// Sentry.init({
//   dsn: 'https://1d96aa7133c14aee878219d206f07e4e@sentry.io/1509937',
//   integrations: [new Integrations.Vue({Vue, attachProps: true})],
// });

export default{
  components: {
    StatsCard,
    ChartCard,
    AnimatedNumber,
    ProductCard,
    AsyncWorldMap,
    Chart
  },
  data () {
    return {
      componentKey: 0,
      componentKey2: 1,
      componentKey3: 2,
      lineChart: [],
      medcoCasesLineChart: [],
      barChart: [],
      barChartColors: [],
      dashboard_stats: {},
      monthly_expert_cases: {},
    }
  },
  methods: {
    notifyVue (verticalAlign, horizontalAlign) {
      if (this.dashboard_stats.total_unresolved_warnings > 0){
        var msg = ''
        if (this.dashboard_stats.total_unresolved_warnings === 1){
          msg = '<span style="color: black">There is ' + this.dashboard_stats.total_unresolved_warnings + ' WARNING awaiting to be resolved!</span>'
        }else{
          msg = '<span style="color: black">There are ' + this.dashboard_stats.total_unresolved_warnings + ' WARNINGS awaiting to be resolved!</span>'
        }
        this.$notify(
        {
          message: msg,
          icon: 'notification_important',
          horizontalAlign: horizontalAlign,
          verticalAlign: verticalAlign,
          type: 'warning',
          
        })

      }
      
    },
  },
  mounted() {
    
  },
  created(){
    console.log("Loading dashboard stats from:", this.url__dashboard_stats)
    this.$http
      .get(this.url__dashboard_stats)
      .then(response => {
        console.log(response.data)
        this.barChart = response.data.bar_chart
        this.medcoCasesLineChart = response.data.medco_cases_line_chart
        this.barChartColors = response.data.bar_chart_colors
        this.lineChart = response.data.line_chart
        this.dashboard_stats = response.data;
        this.notifyVue('top','center')
        this.componentKey += 1
        this.componentKey2 += 1
        this.componentKey3 += 1
      })
      .catch(function(error) {
        console.error(error.response);
      });
  }
}
</script>
<style>
.ct-label{
  font-size: 1.10rem !important;
  font-weight: bold;
}
</style>
