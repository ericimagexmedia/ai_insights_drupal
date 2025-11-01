<?php

namespace Drupal\Tests\smart_analytics_for_drupal\Kernel\Form;

use Drupal\KernelTests\KernelTestBase;
use Symfony\Component\HttpFoundation\Request;
use Drupal\Core\Url;

/**
 * @coversDefaultClass \Drupal\smart_analytics_for_drupal\Form\SettingsForm
 * @group smart_analytics_for_drupal
 */
class SettingsFormTest extends KernelTestBase {

  protected static $modules = [
    'system',
    'user',
    'key',
    'smart_analytics_for_drupal',
  ];

  public function testSettingsFormSubmission(): void {
    // Mock a fake key entity for select options.
    $key_storage = $this->container->get('entity_type.manager')->getStorage('key');
    $key = $key_storage->create(['id' => 'test_key', 'label' => 'Test Key', 'key_type' => 'authentication']);
    $key->save();

    $this->drupalLogin($this->createUser(['administer site configuration']));

    $uri = Url::fromRoute('form.single_form')->toString();
    $this->doRequest(Request::create($uri));

    $values = [
      'ga4_property_id' => 'G-TEST1234',
      'service_account_email' => 'test@project.iam.gserviceaccount.com',
      'project_id' => 'ai-insights',
      'key_reference' => 'test_key',
      'token_uri' => 'https://oauth2.googleapis.com/token',
      'enabled_metrics' => ['screenPageViews' => 'screenPageViews'],
    ];

    $request = Request::create($uri, 'POST', $values);
    $response = $this->doRequest($request);
    $this->assertEquals(303, $response->getStatusCode());

    $config = $this->config('smart_analytics_for_drupal.settings');
    $this->assertEquals('G-TEST1234', $config->get('ga4_property_id'));
    $this->assertEquals('test_key', $config->get('key_reference'));
  }
}
