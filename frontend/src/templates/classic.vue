<template>
  <div class="report-page-wrapper classic-template">
    <div class="report-container" v-if="report">
      <div class="stripe"></div>
      
      <!-- 头部 -->
      <div class="header">
        <div class="header-badge">Annual Report</div>
        <div class="header-star-group">★ ★ ★</div>
        <h1 :class="getTitleClass(report.chat_name)">{{ report.chat_name }}</h1>
        <div class="subtitle">年度报告</div>
        <div class="header-stats">
          <div class="stat-box">
            <div class="stat-value">{{ formatNumber(report.message_count) }}</div>
            <div class="stat-label">消息总数</div>
          </div>
        </div>
      </div>
      
      <div class="stripe-diagonal"></div>
      
      <!-- 柱状图 -->
      <div class="chart-section">
        <div class="section-header">
          <div class="section-title">热词榜</div>
        </div>
        
        <div class="bar-chart">
          <div v-for="(word, index) in report.selected_words" :key="word.word" class="bar-item">
            <div class="bar-value">{{ word.freq }}</div>
            <div class="bar-wrapper">
              <div class="bar" :style="{ height: word.bar_height + '%' }">
                <div v-for="(seg, segIndex) in word.segments" :key="segIndex"
                     class="bar-segment" 
                     :style="{ height: seg.percent + '%', backgroundColor: seg.color }">
                </div>
              </div>
            </div>
            <div class="bar-label">{{ word.word }}</div>
            <div class="bar-rank">#{{ index + 1 }}</div>
            <div class="bar-contributors">
              <div v-for="(item, itemIndex) in word.legend" :key="itemIndex"
                   :class="['bar-contributor-item', { empty: !item.name }]">
                <div class="bar-contributor-dot" :style="{ background: item.color }"></div>
                <span class="bar-contributor-name">{{ item.name }}</span>
              </div>
            </div>
          </div>
        </div>
      </div>
      
      <div class="divider">
        <div class="divider-line"></div>
      </div>
      
      <!-- 热词卡片 -->
      <div class="section">
        <div class="section-header">
          <div class="section-title">热词档案</div>
        </div>
        
        <div class="word-cards">
          <div v-for="(word, index) in report.selected_words" :key="word.word" 
               :class="['word-card', `color-${index + 1}`]">
            <div class="word-card-header">
              <div class="word-card-left">
                <div class="word-card-rank">#{{ index + 1 }}</div>
                <div class="word-card-title">{{ word.word }}</div>
              </div>
              <div class="word-card-freq">{{ word.freq }}次</div>
            </div>
            
            <div v-if="word.ai_comment" class="word-card-comment">{{ word.ai_comment }}</div>
            
            <div class="word-card-contributors">
              {{ word.contributors_text }}
            </div>
            
            <ul class="word-card-samples">
              <li v-for="(sample, sampleIndex) in word.samples.slice(0, 3)" :key="sampleIndex">
                {{ truncateText(sample, 40) }}
              </li>
            </ul>
          </div>
        </div>
      </div>
      
      <div class="stripe"></div>
      
      <!-- 榜单 -->
      <div class="section rankings-section">
        <div class="section-header">
          <div class="section-title">荣誉殿堂</div>
        </div>
        
        <div class="rankings-grid">
          <div v-for="ranking in report.rankings" :key="ranking.title" class="ranking-card">
            <div class="ranking-card-header">
              {{ ranking.icon }} {{ ranking.title }}
            </div>
            
            <div v-if="ranking.first" class="ranking-first">
              <div class="ranking-first-crown">👑</div>
              <img class="ranking-first-avatar" 
                   :src="ranking.first.avatar" 
                   :alt="ranking.first.name"
                   @error="handleImageError">
              <div class="ranking-first-name">{{ ranking.first.name }}</div>
              <div class="ranking-first-value">{{ ranking.first.value }}{{ ranking.unit }}</div>
            </div>
            
            <div v-if="ranking.others" class="ranking-others">
              <div v-for="(item, itemIndex) in ranking.others" :key="itemIndex" class="ranking-item">
                <div class="ranking-item-pos">{{ itemIndex + 2 }}</div>
                <img class="ranking-item-avatar" 
                     :src="item.avatar" 
                     :alt="item.name"
                     @error="handleImageError">
                <div class="ranking-item-name">{{ item.name }}</div>
                <div class="ranking-item-value">{{ item.value }}{{ ranking.unit }}</div>
              </div>
            </div>
          </div>
        </div>
      </div>
      
      <!-- 时段分布 -->
      <div class="section hour-section">
        <div class="section-header">
          <div class="section-title">活跃时段</div>
        </div>
        
        <div class="hour-chart-container">
          <div class="hour-chart">
            <div v-for="(hour, index) in report.statistics?.hourDistribution || {}" :key="index"
                 class="hour-bar" :style="{ height: getHourHeightPercent(hour) + '%' }"></div>
          </div>
          <div class="hour-labels">
            <span>0时</span>
            <span>6时</span>
            <span>12时</span>
            <span>18时</span>
            <span>24时</span>
          </div>
          <div class="hour-peak">
            ⭐ 最活跃时段
            <div class="hour-peak-badge">{{ peakHourText }}</div>
          </div>
        </div>
      </div>
      
      <div class="stripe-diagonal"></div>
      
      <!-- 分享按钮区域 -->
      <div class="share-section">
        <div class="share-container">
          <!-- 如果没有生成图片或有错误，显示生成按钮 -->
          <button 
            v-if="!imageUrl || imageError"
            class="share-button" 
            @click="$emit('generate-image')"
            :disabled="generatingImage">
            <span v-if="!generatingImage">
              {{ imageError ? '🔄 重新生成' : '📸 生成图片分享' }}
            </span>
            <span v-else>
              <span class="loading-dots">生成中</span>
            </span>
          </button>
          
          <!-- 如果图片已生成，显示下载和重新生成选项 -->
          <div v-if="imageUrl && !imageError" class="share-result">
            <div class="share-success">✅ 图片已生成并下载</div>
            <div class="share-actions">
              <a :href="imageUrl" :download="imageFileName" class="download-button">
                💾 再次下载
              </a>
              <button class="regenerate-button" @click="$emit('generate-image')">
                🔄 重新生成
              </button>
            </div>
          </div>
          
          <!-- 显示错误信息 -->
          <div v-if="imageError" class="share-error">
            ❌ {{ imageError }}
          </div>
        </div>
      </div>
      
      <!-- 页脚 -->
      <div class="footer">
        <div class="footer-text">
          Github.com/ZiHuixi/QQgroup-annual-report-analyzer
        </div>
      </div>
      
      <div class="stripe-thin"></div>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { useReportUtils } from '../composables/useReportUtils'

// ========== Props ==========
const props = defineProps({
  report: {
    type: Object,
    required: true
  },
  generatingImage: {
    type: Boolean,
    default: false
  },
  imageUrl: {
    type: String,
    default: ''
  },
  imageError: {
    type: String,
    default: ''
  }
})

// ========== Emits ==========
defineEmits(['generate-image'])

// ========== 使用工具函数 ==========
const {
  formatNumber,
  truncateText,
  getTitleClass,
  handleImageError,
  getHourHeight,
  getPeakHour
} = useReportUtils()

// ========== 计算属性 ==========
// 获取时段高度百分比
const getHourHeightPercent = (hour) => {
  return getHourHeight(hour, props.report.statistics?.hourDistribution)
}

// 获取最活跃时段文本
const peakHourText = computed(() => {
  const peak = getPeakHour(props.report.statistics?.hourDistribution)
  return `${peak}:00 - ${peak + 1}:00`
})

// 获取图片文件名
const imageFileName = computed(() => {
  const chatName = props.report?.chat_name || '报告'
  return `${chatName}_年度报告_${new Date().getTime()}.png`
})
</script>

<style>
@import '../report-styles.css';
</style>

<style scoped>
.classic-template {
  
}
</style>
