<?php
namespace Drupal\smart_analytics_for_drupal\Controller;

use Drupal\Core\Controller\ControllerBase;
use Symfony\Component\HttpFoundation\JsonResponse;
use Drupal\key\KeyRepositoryInterface;
use Symfony\Component\DependencyInjection\ContainerInterface;

class KeyRefreshController extends ControllerBase {

  /**
   * @var \Drupal\key\KeyRepositoryInterface
   */
  protected KeyRepositoryInterface $keyRepository;

  /**
   * The Constructor.
   * @param \Drupal\key\KeyRepositoryInterface $keyRepository
   *  The key repository.
   */
  public function __construct(KeyRepositoryInterface $keyRepository) {
    $this->keyRepository = $keyRepository;
  }

  /**
   * {@inheritdoc}
   */
  public static function create(ContainerInterface $container) {
    return new static(
      $container->get('key.repository')
    );
  }

  /**
   * Refresh the list of keys via AJAX.
   * @return \Symfony\Component\HttpFoundation\JsonResponse
   *  The JSON response containing the updated keys.
   */
  public function refreshKeys(): JsonResponse {
    $keys = $this->keyRepository->getKeysByType('authentication');
    $options = [];
    $last_created = NULL;
    foreach ($keys as $key) {
      $options[$key->id()] = $key->label();
      $last_created = $key->id();
    }
    return new JsonResponse([
      'options' => $options,
      'last_created' => $last_created,
    ]);
  }
}
