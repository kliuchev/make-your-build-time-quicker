import Feature08Domain
import Feature08Data

public enum Feature08PresentationScreen {
    public static func render(_ id: Int) -> String {
        let model: Feature08DomainModel = Feature08DataRepository.load(id)
        return "\(model.title):\(model.score)"
    }

}
