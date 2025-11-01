<?php

namespace Drupal\smart_analytics_for_drupal\Form;

use Drupal\Core\Form\ConfigFormBase;
use Drupal\Core\Form\FormStateInterface;
use Drupal\key\Entity\Key;
use Drupal\key\KeyRepositoryInterface;
use Symfony\Component\DependencyInjection\ContainerInterface;
use Drupal\Core\Link;
use Drupal\Core\Url;

/**
 * Defines the settings form for Smart Analytics for Drupal.
 */
class SettingsForm extends ConfigFormBase {

  /**
   * @var \Drupal\key\KeyRepositoryInterface
   */
  protected KeyRepositoryInterface $keyRepository;

  public static function create(ContainerInterface $container) {
    $instance = parent::create($container);
    $instance->keyRepository = $container->get('key.repository');
    return $instance;
  }

  /**
   * {@inheritdoc}
   */
  public function getFormId(): string {
    return 'smart_analytics_for_drupal_settings_form';
  }

  /**
   * {@inheritdoc}
   */
  protected function getEditableConfigNames(): array {
    return ['smart_analytics_for_drupal.settings'];
  }

  /**
   * {@inheritdoc}
   */
  public function buildForm(array $form, FormStateInterface $form_state): array {
    $config = $this->config('smart_analytics_for_drupal.settings');

    // -----------------------------
    // GA4 PROPERTY CONFIGURATION
    // -----------------------------
    $form['ga4'] = [
      '#type' => 'details',
      '#title' => $this->t('Google Analytics 4 Property'),
      '#open' => TRUE,
    ];

    $form['ga4']['ga4_property_id'] = [
      '#type' => 'textfield',
      '#title' => $this->t('GA4 Property ID'),
      '#description' => $this->t('Enter your GA4 Measurement ID (e.g. G-XXXXXXX).'),
      '#default_value' => $config->get('ga4_property_id'),
      '#required' => TRUE,
    ];

    // -----------------------------
    // CREATE VERTICAL TABS
    // -----------------------------
    $form['settings_tabs'] = [
      '#type' => 'vertical_tabs',
      '#title' => $this->t('Settings'),
      '#description' => $this->t('Configure connection and advanced options for Smart Analytics.'),
      '#description_display' => 'before',
      '#weight' => 20,
    ];

    // -----------------------------
    // TAB 1: SERVICE ACCOUNT
    // -----------------------------
    $form['service_account'] = [
      '#type' => 'details',
      '#title' => $this->t('Service Account Credentials'),
      '#group' => 'settings_tabs',
    ];

    $form['service_account']['service_account_email'] = [
      '#type' => 'email',
      '#title' => $this->t('Service Account Email'),
      '#default_value' => $config->get('service_account_email'),
      '#description' => $this->t('The client_email from your Google Cloud service account JSON file.'),
      '#required' => TRUE,
    ];

    $form['service_account']['project_id'] = [
      '#type' => 'textfield',
      '#title' => $this->t('Project ID'),
      '#default_value' => $config->get('project_id'),
      '#description' => $this->t('The project_id associated with your Google Cloud project.'),
    ];

    $keys = $this->keyRepository->getKeysByType('authentication');
    $options = [];
    foreach ($keys as $key) {
      $options[$key->id()] = $key->label();
    }


    $create_key_url = Url::fromRoute('entity.key.add_form',
      ['key_type' => 'authentication',], [
      'attributes' => [
        'class' => ['use-ajax'],
        'data-dialog-type' => 'modal',
        'data-dialog-options' => json_encode(['width' => 700]),
      ],
    ]);

    $create_key_link = Link::fromTextAndUrl($this->t('Create new key'), $create_key_url)->toString();

    $form['service_account']['key_reference'] = [
      '#type' => 'select',
      '#title' => $this->t('Private Key'),
      '#options' => $options,
      '#default_value' => $config->get('key_reference'),
      '#description' => $this->t('Select an existing key, or @link.', [
        '@link' => $create_key_link,
      ]),
      '#required' => TRUE,
      '#suffix' => '<div class="description">' . $this->t('If you create a new key, reload this page afterward to see it in the list.') . '</div>',
    ];

    // -----------------------------
    // TAB 2: ADVANCED SETTINGS
    // -----------------------------
    $form['advanced'] = [
      '#type' => 'details',
      '#title' => $this->t('Advanced Settings'),
      '#group' => 'settings_tabs',
    ];

    $form['advanced']['token_uri'] = [
      '#type' => 'textfield',
      '#title' => $this->t('Token URI'),
      '#default_value' => $config->get('token_uri') ?? 'https://oauth2.googleapis.com/token',
      '#description' => $this->t('Usually this should remain as the default value.'),
    ];

    $form['advanced']['enabled_metrics'] = [
      '#type' => 'checkboxes',
      '#title' => $this->t('Enabled Metrics'),
      '#default_value' => $config->get('enabled_metrics') ?? [],
      '#options' => [
        'screenPageViews' => $this->t('Page Views'),
        'averageSessionDuration' => $this->t('Average Session Duration'),
        'userEngagementDuration' => $this->t('User Engagement Duration'),
        'bounceRate' => $this->t('Bounce Rate'),
      ],
      '#description' => $this->t('Select which metrics should be collected and displayed.'),
    ];

    return parent::buildForm($form, $form_state);
  }

  /**
   * {@inheritdoc}
   */
  public function submitForm(array &$form, FormStateInterface $form_state): void {
    $this->configFactory->getEditable('smart_analytics_for_drupal.settings')
      ->set('ga4_property_id', $form_state->getValue('ga4_property_id'))
      ->set('service_account_email', $form_state->getValue('service_account_email'))
      ->set('project_id', $form_state->getValue('project_id'))
      ->set('key_reference', $form_state->getValue('key_reference'))
      ->set('token_uri', $form_state->getValue('token_uri'))
      ->set('enabled_metrics', array_filter($form_state->getValue('enabled_metrics')))
      ->save();

    parent::submitForm($form, $form_state);
  }

}
