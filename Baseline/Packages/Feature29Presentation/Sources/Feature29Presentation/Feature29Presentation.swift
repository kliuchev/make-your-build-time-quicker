import Feature29Domain
import Feature29Data

public enum Feature29PresentationScreen {
    public static func render(_ id: Int) -> String {
        let model: Feature29DomainModel = Feature29DataRepository.load(id)
        return "\(model.title):\(model.score)"
    }

}
