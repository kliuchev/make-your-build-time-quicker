import Feature15Domain
import Feature15Data

public enum Feature15PresentationScreen {
    public static func render(_ id: Int) -> String {
        let model: Feature15DomainModel = Feature15DataRepository.load(id)
        return "\(model.title):\(model.score)"
    }

}
