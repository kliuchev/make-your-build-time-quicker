import Feature06Domain
import Feature06Data

public enum Feature06PresentationScreen {
    public static func render(_ id: Int) -> String {
        let model: Feature06DomainModel = Feature06DataRepository.load(id)
        return "\(model.title):\(model.score)"
    }

}
